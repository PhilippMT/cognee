"""
Get router for the ADHD Thought Graph API.

This module provides REST API endpoints for managing ADHD-optimized thought graphs,
including thought capture, connection discovery, graph enrichment, web research,
project matching, and edge weight management.
"""

from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry
from cognee import __version__ as cognee_version
from cognee.shared.logging_utils import get_logger

logger = get_logger("api.thought_graph")


# ============================================================================
# Request/Response DTOs
# ============================================================================

class AddThoughtPayloadDTO(InDTO):
    """Payload for adding a new thought to the graph."""
    content: str = Field(..., description="The thought content text")
    tags: Optional[List[str]] = Field(default=None, description="Tags for categorization")
    energy_level: Optional[int] = Field(
        default=None, ge=1, le=10, description="Energy level (1-10) when thought was captured"
    )
    importance_score: Optional[int] = Field(
        default=None, ge=1, le=10, description="Importance rating (1-10)"
    )
    auto_connect: bool = Field(
        default=True, description="Automatically discover and create connections"
    )
    similarity_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Minimum similarity for auto-connections"
    )


class BatchAddThoughtsPayloadDTO(InDTO):
    """Payload for adding multiple thoughts in batch."""
    thoughts: List[AddThoughtPayloadDTO] = Field(..., description="List of thoughts to add")


class DiscoverConnectionsPayloadDTO(InDTO):
    """Payload for discovering connections for a specific thought."""
    thought_id: str = Field(..., description="ID of the thought to discover connections for")
    similarity_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Minimum similarity threshold"
    )
    max_connections: int = Field(default=10, description="Maximum connections to discover")


class EnrichGraphPayloadDTO(InDTO):
    """Payload for enriching the thought graph with algorithms."""
    compute_pagerank: bool = Field(default=True, description="Compute PageRank scores")
    compute_centrality: bool = Field(default=True, description="Compute centrality measures")
    detect_communities: bool = Field(default=True, description="Detect thought communities")
    find_transitive: bool = Field(default=True, description="Find transitive connections")
    auto_add_transitive_links: bool = Field(
        default=False, description="Automatically create transitive connections"
    )


class WebEnrichmentPayloadDTO(InDTO):
    """Payload for enriching thoughts with web search."""
    thought_id: str = Field(..., description="ID of the thought to enrich")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum web search results")
    search_depth: str = Field(
        default="basic", description="Search depth: 'basic' or 'advanced'"
    )


class BatchWebEnrichmentPayloadDTO(InDTO):
    """Payload for batch web enrichment."""
    thought_ids: List[str] = Field(..., description="List of thought IDs to enrich")
    max_results_per_thought: int = Field(
        default=3, ge=1, le=10, description="Max results per thought"
    )


class ProjectMatchingPayloadDTO(InDTO):
    """Payload for matching thoughts to projects."""
    project_patterns: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Custom project patterns: {'project_name': ['keyword1', 'keyword2']}"
    )
    auto_detect_repos: bool = Field(
        default=True, description="Auto-detect GitHub/GitLab repository mentions"
    )


class EdgeDecayPayloadDTO(InDTO):
    """Payload for decaying edge weights based on time."""
    decay_rate: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Decay rate per day"
    )
    min_weight: float = Field(
        default=0.15, ge=0.0, le=1.0, description="Minimum weight before removal"
    )
    days_threshold: int = Field(
        default=30, ge=1, description="Days since last update for decay"
    )


class ReinforceEdgePayloadDTO(InDTO):
    """Payload for reinforcing a specific edge."""
    source_id: str = Field(..., description="Source thought ID")
    target_id: str = Field(..., description="Target thought ID")
    reinforcement_amount: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Amount to increase weight"
    )


class MemifyPayloadDTO(InDTO):
    """Payload for integrated memify operation."""
    enable_web_enrichment: bool = Field(default=False, description="Enable web search enrichment")
    enable_project_matching: bool = Field(default=True, description="Enable project matching")
    enable_edge_decay: bool = Field(default=True, description="Enable edge weight decay")
    enable_potential_connections: bool = Field(
        default=True, description="Calculate potential connections"
    )
    project_patterns: Optional[Dict[str, List[str]]] = Field(
        default=None, description="Custom project patterns"
    )
    web_search_top_k: int = Field(default=5, description="Top K thoughts to enrich with web")


class ThoughtResponseDTO(OutDTO):
    """Response DTO for a thought node."""
    id: str
    content: str
    tags: Optional[List[str]]
    energy_level: Optional[int]
    importance_score: Optional[int]
    created_at: datetime
    updated_at: datetime
    pagerank_score: Optional[float] = None
    betweenness_centrality: Optional[float] = None
    community_id: Optional[int] = None


class ConnectionResponseDTO(OutDTO):
    """Response DTO for a connection."""
    source_id: str
    target_id: str
    relationship_type: str
    discovery_method: str
    strength: float
    explanation: Optional[str] = None


class SurpriseConnectionResponseDTO(OutDTO):
    """Response DTO for a surprise connection."""
    thought1_id: str
    thought2_id: str
    surprise_score: float
    semantic_distance: float
    temporal_distance: Optional[float] = None
    explanation: str


class EnrichmentResultsResponseDTO(OutDTO):
    """Response DTO for enrichment results."""
    pagerank_scores: Optional[Dict[str, float]] = None
    centrality_scores: Optional[Dict[str, Any]] = None
    communities: Optional[Dict[int, List[str]]] = None
    transitive_connections: Optional[List[Dict[str, str]]] = None
    processing_time: float


class ProjectMatchResponseDTO(OutDTO):
    """Response DTO for project matching results."""
    project_matches: Dict[str, List[Dict[str, Any]]]
    total_matches: int


class WebEnrichmentResponseDTO(OutDTO):
    """Response DTO for web enrichment results."""
    thought_id: str
    search_results: List[Dict[str, Any]]
    enrichment_status: str


# ============================================================================
# Router Definition
# ============================================================================

def get_thought_graph_router() -> APIRouter:
    """
    Returns the FastAPI router for ADHD Thought Graph management.

    This router provides endpoints for managing thoughts, discovering connections,
    enriching graphs with algorithms, web research, project matching, and edge management.
    """
    router = APIRouter()

    # ========================================================================
    # Thought Management Endpoints
    # ========================================================================

    @router.post("/thoughts", response_model=ThoughtResponseDTO)
    async def add_thought(
        payload: AddThoughtPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Add a new thought to the ADHD thought graph.

        This endpoint creates a new thought node with ADHD-optimized fields including
        energy level, importance score, and automatic connection discovery.

        ## Request Parameters
        - **content** (str): The thought content text (required)
        - **tags** (Optional[List[str]]): Tags for categorization
        - **energy_level** (Optional[int]): Energy level (1-10) when thought was captured
        - **importance_score** (Optional[int]): Importance rating (1-10)
        - **auto_connect** (bool): Automatically discover and create connections (default: true)
        - **similarity_threshold** (float): Minimum similarity for auto-connections (0.0-1.0)

        ## Response
        Returns the created thought with ID and metadata.

        ## Error Codes
        - **400 Bad Request**: Invalid parameters (e.g., empty content, out-of-range values)
        - **409 Conflict**: Error during thought creation or connection discovery
        - **500 Internal Server Error**: Unexpected error

        ## Example Request
        ```json
        {
            "content": "Build graph database for ADHD thought management",
            "tags": ["adhd", "productivity", "graph-db"],
            "energy_level": 7,
            "importance_score": 9,
            "auto_connect": true,
            "similarity_threshold": 0.7
        }
        ```
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/thoughts",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import add_thought as add_thought_op

            thought_node = await add_thought_op(
                content=payload.content,
                tags=payload.tags,
                energy_level=payload.energy_level,
                importance_score=payload.importance_score,
                auto_connect=payload.auto_connect,
                similarity_threshold=payload.similarity_threshold,
            )

            return ThoughtResponseDTO(
                id=thought_node.id,
                content=thought_node.content,
                tags=thought_node.tags,
                energy_level=thought_node.energy_level,
                importance_score=thought_node.importance_score,
                created_at=thought_node.created_at,
                updated_at=thought_node.updated_at,
                pagerank_score=thought_node.pagerank_score,
                betweenness_centrality=thought_node.betweenness_centrality,
                community_id=thought_node.community_id,
            )
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error adding thought: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.post("/thoughts/batch", response_model=List[ThoughtResponseDTO])
    async def add_thoughts_batch(
        payload: BatchAddThoughtsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Add multiple thoughts to the graph in batch.

        This endpoint efficiently creates multiple thought nodes at once, with optional
        automatic connection discovery.

        ## Request Parameters
        - **thoughts** (List[AddThoughtPayloadDTO]): List of thoughts to add

        ## Response
        Returns list of created thoughts with IDs and metadata.

        ## Error Codes
        - **400 Bad Request**: Invalid parameters in one or more thoughts
        - **409 Conflict**: Error during batch creation
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/thoughts/batch",
                "cognee_version": cognee_version,
                "batch_size": len(payload.thoughts),
            },
        )

        try:
            from cognee.modules.thought_graph.operations import add_thoughts_batch as batch_op

            thought_nodes = await batch_op(
                thoughts=[
                    {
                        "content": t.content,
                        "tags": t.tags,
                        "energy_level": t.energy_level,
                        "importance_score": t.importance_score,
                    }
                    for t in payload.thoughts
                ]
            )

            return [
                ThoughtResponseDTO(
                    id=node.id,
                    content=node.content,
                    tags=node.tags,
                    energy_level=node.energy_level,
                    importance_score=node.importance_score,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                )
                for node in thought_nodes
            ]
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error adding thoughts batch: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Connection Discovery Endpoints
    # ========================================================================

    @router.post("/connections/discover", response_model=List[ConnectionResponseDTO])
    async def discover_connections(
        payload: DiscoverConnectionsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Discover connections for a specific thought.

        Uses semantic similarity, tag overlap, and LLM inference to find related thoughts
        and create connections.

        ## Request Parameters
        - **thought_id** (str): ID of the thought to discover connections for
        - **similarity_threshold** (float): Minimum similarity threshold (0.0-1.0)
        - **max_connections** (int): Maximum connections to discover

        ## Response
        Returns list of discovered connections.

        ## Error Codes
        - **404 Not Found**: Thought ID doesn't exist
        - **409 Conflict**: Error during connection discovery
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/connections/discover",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import discover_connections as discover_op

            connections = await discover_op(
                thought_id=payload.thought_id,
                similarity_threshold=payload.similarity_threshold,
                max_connections=payload.max_connections,
            )

            return [
                ConnectionResponseDTO(
                    source_id=conn.source_id,
                    target_id=conn.target_id,
                    relationship_type=conn.relationship_type,
                    discovery_method=conn.discovery_method,
                    strength=conn.strength,
                    explanation=conn.explanation,
                )
                for conn in connections
            ]
        except Exception as error:
            logger.error(f"Error discovering connections: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.get("/connections/surprise", response_model=List[SurpriseConnectionResponseDTO])
    async def find_surprise_connections(
        min_surprise_score: float = 0.6,
        limit: int = 10,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Find surprise connections with high semantic or temporal distance.

        These connections represent non-obvious relationships that can spark insights
        and leverage ADHD strengths in pattern recognition.

        ## Query Parameters
        - **min_surprise_score** (float): Minimum surprise score threshold (default: 0.6)
        - **limit** (int): Maximum number of surprise connections to return (default: 10)

        ## Response
        Returns list of surprise connections with scores and explanations.

        ## Error Codes
        - **409 Conflict**: Error finding surprise connections
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "GET /v1/thought_graph/connections/surprise",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import find_surprise_connections as surprise_op

            surprises = await surprise_op(
                min_surprise_score=min_surprise_score,
                limit=limit,
            )

            return [
                SurpriseConnectionResponseDTO(
                    thought1_id=s.thought1_id,
                    thought2_id=s.thought2_id,
                    surprise_score=s.surprise_score,
                    semantic_distance=s.semantic_distance,
                    temporal_distance=s.temporal_distance,
                    explanation=s.explanation,
                )
                for s in surprises
            ]
        except Exception as error:
            logger.error(f"Error finding surprise connections: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Graph Enrichment Endpoints
    # ========================================================================

    @router.post("/enrich", response_model=EnrichmentResultsResponseDTO)
    async def enrich_graph(
        payload: EnrichGraphPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Enrich the thought graph with graph algorithms.

        Runs PageRank, centrality measures, community detection, and transitive
        connection discovery to identify influential thoughts, bridge ideas,
        and thematic clusters.

        ## Request Parameters
        - **compute_pagerank** (bool): Compute PageRank scores (default: true)
        - **compute_centrality** (bool): Compute centrality measures (default: true)
        - **detect_communities** (bool): Detect thought communities (default: true)
        - **find_transitive** (bool): Find transitive connections (default: true)
        - **auto_add_transitive_links** (bool): Auto-create transitive links (default: false)

        ## Response
        Returns enrichment results including scores, communities, and processing time.

        ## Error Codes
        - **409 Conflict**: Error during graph enrichment
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/enrich",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import enrich_thought_graph
            import time

            start_time = time.time()

            results = await enrich_thought_graph(
                compute_pagerank=payload.compute_pagerank,
                compute_centrality=payload.compute_centrality,
                detect_communities_flag=payload.detect_communities,
                find_transitive=payload.find_transitive,
                auto_add_transitive_links=payload.auto_add_transitive_links,
            )

            processing_time = time.time() - start_time

            return EnrichmentResultsResponseDTO(
                pagerank_scores=results.get("pagerank_scores"),
                centrality_scores=results.get("centrality_scores"),
                communities=results.get("communities"),
                transitive_connections=results.get("transitive_connections"),
                processing_time=processing_time,
            )
        except Exception as error:
            logger.error(f"Error enriching graph: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Web Enrichment Endpoints
    # ========================================================================

    @router.post("/enrich/web", response_model=WebEnrichmentResponseDTO)
    async def enrich_with_web(
        payload: WebEnrichmentPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Enrich a thought with web search results.

        Uses Tavily API to perform deep web research and link external knowledge
        to the thought. Requires TAVILY_API_KEY environment variable.

        ## Request Parameters
        - **thought_id** (str): ID of the thought to enrich
        - **max_results** (int): Maximum web search results (1-20, default: 5)
        - **search_depth** (str): Search depth 'basic' or 'advanced' (default: 'basic')

        ## Response
        Returns web enrichment results with search data.

        ## Error Codes
        - **400 Bad Request**: Missing TAVILY_API_KEY
        - **404 Not Found**: Thought ID doesn't exist
        - **409 Conflict**: Error during web enrichment
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/enrich/web",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import enrich_with_web_search

            result = await enrich_with_web_search(
                thought_id=payload.thought_id,
                max_results=payload.max_results,
                search_depth=payload.search_depth,
            )

            return WebEnrichmentResponseDTO(
                thought_id=payload.thought_id,
                search_results=result.get("search_results", []),
                enrichment_status=result.get("status", "completed"),
            )
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error enriching with web: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.post("/enrich/web/batch", response_model=List[WebEnrichmentResponseDTO])
    async def batch_enrich_with_web(
        payload: BatchWebEnrichmentPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Enrich multiple thoughts with web search results in batch.

        Efficiently performs web research for multiple thoughts at once.

        ## Request Parameters
        - **thought_ids** (List[str]): List of thought IDs to enrich
        - **max_results_per_thought** (int): Max results per thought (1-10, default: 3)

        ## Response
        Returns list of web enrichment results.

        ## Error Codes
        - **400 Bad Request**: Missing TAVILY_API_KEY
        - **409 Conflict**: Error during batch web enrichment
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/enrich/web/batch",
                "cognee_version": cognee_version,
                "batch_size": len(payload.thought_ids),
            },
        )

        try:
            from cognee.modules.thought_graph.operations import batch_enrich_with_web as batch_web_op

            results = await batch_web_op(
                thought_ids=payload.thought_ids,
                max_results=payload.max_results_per_thought,
            )

            return [
                WebEnrichmentResponseDTO(
                    thought_id=r.get("thought_id"),
                    search_results=r.get("search_results", []),
                    enrichment_status=r.get("status", "completed"),
                )
                for r in results
            ]
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error batch enriching with web: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Project Matching Endpoints
    # ========================================================================

    @router.post("/projects/match", response_model=ProjectMatchResponseDTO)
    async def match_projects(
        payload: ProjectMatchingPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Match thoughts to projects and repositories.

        Auto-detects GitHub/GitLab repository mentions and matches thoughts to
        custom project patterns.

        ## Request Parameters
        - **project_patterns** (Optional[Dict]): Custom project patterns mapping
        - **auto_detect_repos** (bool): Auto-detect GitHub/GitLab repos (default: true)

        ## Response
        Returns project matches with confidence scores.

        ## Error Codes
        - **409 Conflict**: Error during project matching

        ## Example Request
        ```json
        {
            "project_patterns": {
                "cognee": ["cognee", "knowledge graph", "memory"],
                "backend-api": ["api", "server", "fastapi"]
            },
            "auto_detect_repos": true
        }
        ```
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/projects/match",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import match_to_projects

            matches = await match_to_projects(
                project_patterns=payload.project_patterns,
                auto_detect_repos=payload.auto_detect_repos,
            )

            return ProjectMatchResponseDTO(
                project_matches=matches,
                total_matches=sum(len(v) for v in matches.values()),
            )
        except Exception as error:
            logger.error(f"Error matching projects: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Edge Weight Management Endpoints
    # ========================================================================

    @router.post("/edges/decay", response_model=dict)
    async def decay_edges(
        payload: EdgeDecayPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Decay edge weights based on time since last update.

        Implements time-based decay where older connections gradually weaken
        and are removed when weight drops below minimum threshold.

        ## Request Parameters
        - **decay_rate** (float): Decay rate per day (0.0-1.0, default: 0.1)
        - **min_weight** (float): Minimum weight before removal (0.0-1.0, default: 0.15)
        - **days_threshold** (int): Days since last update for decay (default: 30)

        ## Response
        Returns decay operation results including edges affected and removed.

        ## Error Codes
        - **400 Bad Request**: Invalid parameters
        - **409 Conflict**: Error during edge decay
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/edges/decay",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import decay_edge_weights

            results = await decay_edge_weights(
                decay_rate=payload.decay_rate,
                min_weight=payload.min_weight,
                days_threshold=payload.days_threshold,
            )

            return results
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error decaying edges: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.post("/edges/reinforce", response_model=dict)
    async def reinforce_edge(
        payload: ReinforceEdgePayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Reinforce a specific edge by increasing its weight.

        Strengthens important connections to prevent them from being pruned.

        ## Request Parameters
        - **source_id** (str): Source thought ID
        - **target_id** (str): Target thought ID
        - **reinforcement_amount** (float): Amount to increase weight (0.0-1.0, default: 0.1)

        ## Response
        Returns reinforcement results.

        ## Error Codes
        - **400 Bad Request**: Invalid parameters
        - **404 Not Found**: Edge doesn't exist
        - **409 Conflict**: Error during edge reinforcement
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/edges/reinforce",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import reinforce_edge as reinforce_op

            result = await reinforce_op(
                source_id=payload.source_id,
                target_id=payload.target_id,
                reinforcement_amount=payload.reinforcement_amount,
            )

            return result
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as error:
            logger.error(f"Error reinforcing edge: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.get("/edges/potential", response_model=List[dict])
    async def get_potential_connections(
        min_potential_score: float = 0.5,
        limit: int = 20,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Calculate potential connections with weighted suggestions.

        Discovers missing links in the graph based on graph topology,
        semantic similarity, and tag overlap.

        ## Query Parameters
        - **min_potential_score** (float): Minimum potential score (default: 0.5)
        - **limit** (int): Maximum potential connections to return (default: 20)

        ## Response
        Returns list of potential connections with scores.

        ## Error Codes
        - **409 Conflict**: Error calculating potential connections
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "GET /v1/thought_graph/edges/potential",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import calculate_potential_connections

            potentials = await calculate_potential_connections(
                min_potential_score=min_potential_score,
                limit=limit,
            )

            return potentials
        except Exception as error:
            logger.error(f"Error calculating potential connections: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Integrated Memify Endpoint
    # ========================================================================

    @router.post("/memify", response_model=dict)
    async def memify(
        payload: MemifyPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Integrated memify operation for comprehensive thought graph enrichment.

        Runs all enrichment phases in one command: graph algorithms, web search,
        project matching, edge decay, and potential connection discovery.

        ## Request Parameters
        - **enable_web_enrichment** (bool): Enable web search (default: false, requires TAVILY_API_KEY)
        - **enable_project_matching** (bool): Enable project matching (default: true)
        - **enable_edge_decay** (bool): Enable edge weight decay (default: true)
        - **enable_potential_connections** (bool): Calculate potential connections (default: true)
        - **project_patterns** (Optional[Dict]): Custom project patterns
        - **web_search_top_k** (int): Top K thoughts to enrich with web (default: 5)

        ## Response
        Returns comprehensive memify results from all enabled phases.

        ## Error Codes
        - **409 Conflict**: Error during memify operation

        ## Example Request
        ```json
        {
            "enable_web_enrichment": true,
            "enable_project_matching": true,
            "enable_edge_decay": true,
            "enable_potential_connections": true,
            "project_patterns": {
                "cognee": ["cognee", "knowledge graph"]
            },
            "web_search_top_k": 5
        }
        ```
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/thought_graph/memify",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import memify_thoughts

            results = await memify_thoughts(
                enable_web_enrichment=payload.enable_web_enrichment,
                enable_project_matching=payload.enable_project_matching,
                enable_edge_decay=payload.enable_edge_decay,
                enable_potential_connections=payload.enable_potential_connections,
                project_patterns=payload.project_patterns,
                web_search_top_k=payload.web_search_top_k,
            )

            return results
        except Exception as error:
            logger.error(f"Error during memify: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    # ========================================================================
    # Graph Exploration Endpoints
    # ========================================================================

    @router.get("/thoughts/{thought_id}/neighbors", response_model=List[ThoughtResponseDTO])
    async def get_neighbors(
        thought_id: str,
        max_hops: int = 1,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get neighboring thoughts for a specific thought.

        Returns thoughts connected to the specified thought up to max_hops distance.

        ## Path Parameters
        - **thought_id** (str): ID of the thought

        ## Query Parameters
        - **max_hops** (int): Maximum hops from the thought (default: 1)

        ## Response
        Returns list of neighboring thoughts.

        ## Error Codes
        - **404 Not Found**: Thought ID doesn't exist
        - **409 Conflict**: Error getting neighbors
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": f"GET /v1/thought_graph/thoughts/{thought_id}/neighbors",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import get_thought_neighbors

            neighbors = await get_thought_neighbors(
                thought_id=thought_id,
                max_hops=max_hops,
            )

            return [
                ThoughtResponseDTO(
                    id=node.id,
                    content=node.content,
                    tags=node.tags,
                    energy_level=node.energy_level,
                    importance_score=node.importance_score,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                )
                for node in neighbors
            ]
        except Exception as error:
            logger.error(f"Error getting neighbors: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    @router.get("/communities", response_model=dict)
    async def get_communities(
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get thought communities detected in the graph.

        Returns thematic clusters of related thoughts identified by community
        detection algorithms.

        ## Response
        Returns communities with member thoughts.

        ## Error Codes
        - **409 Conflict**: Error getting communities
        """
        send_telemetry(
            "Thought Graph API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "GET /v1/thought_graph/communities",
                "cognee_version": cognee_version,
            },
        )

        try:
            from cognee.modules.thought_graph.operations import get_thought_communities

            communities = await get_thought_communities()

            return communities
        except Exception as error:
            logger.error(f"Error getting communities: {error}")
            return JSONResponse(status_code=409, content={"error": str(error)})

    return router
