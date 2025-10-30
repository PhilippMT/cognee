"""
Episode-Based Endpoints with Graphiti Temporal Awareness

This module provides API endpoints for episode-based temporal memory using Graphiti.
Episodes are temporal units of information that can be added to the graph with timestamps.
"""

from uuid import UUID
from typing import Optional, List
from datetime import datetime
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


class EpisodeDTO(BaseModel):
    """Episode data transfer object."""
    name: str = Field(..., description="Unique name for this episode")
    text: str = Field(..., description="Text content of the episode")
    source_description: Optional[str] = Field(
        default="user_input",
        description="Description of the episode source"
    )
    reference_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp for this episode (defaults to current time)"
    )


class AddEpisodesPayloadDTO(InDTO):
    """Request payload for adding episodes."""
    episodes: List[EpisodeDTO] = Field(
        ...,
        description="List of episodes to add to the temporal graph"
    )
    dataset: Optional[str] = Field(
        default=None,
        description="Optional dataset name to organize episodes"
    )


class AddEpisodesResponseDTO(OutDTO):
    """Response for adding episodes."""
    message: str
    episodes_added: int
    dataset: Optional[str]
    status: str


class SearchEpisodesPayloadDTO(InDTO):
    """Request payload for searching episodes."""
    query: str = Field(..., description="Search query text")
    time_from: Optional[datetime] = Field(
        default=None,
        description="Start time filter (optional)"
    )
    time_to: Optional[datetime] = Field(
        default=None,
        description="End time filter (optional)"
    )
    top_k: int = Field(default=10, ge=1, le=100, description="Maximum results to return")


class EpisodeSearchResultDTO(OutDTO):
    """Episode search result."""
    name: str
    content: str
    summary: Optional[str] = None
    timestamp: Optional[datetime] = None
    relevance_score: float


class SearchEpisodesResponseDTO(OutDTO):
    """Response for episode search."""
    results: List[EpisodeSearchResultDTO]
    query: str
    total_results: int


def get_episode_endpoints_router() -> APIRouter:
    """Create and return the episode endpoints router."""
    router = APIRouter()

    @router.post("/add", response_model=AddEpisodesResponseDTO)
    async def add_episodes(
        payload: AddEpisodesPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Add episodes to the temporal graph using Graphiti.

        Episodes are temporal units of information that can be queried with
        time-aware context. Each episode is indexed with a timestamp and can
        be retrieved based on temporal proximity.

        ## Request Parameters
        - **episodes** (List[EpisodeDTO]): List of episodes to add
          - **name**: Unique identifier for the episode
          - **text**: Text content of the episode
          - **source_description**: Description of where this episode came from
          - **reference_time**: Timestamp for temporal indexing (optional)
        - **dataset** (Optional[str]): Dataset to organize episodes

        ## Response
        Returns confirmation of episodes added.

        ## Features
        - Temporal indexing with reference times
        - Automatic entity and relationship extraction
        - Time-aware context building
        - Integration with cognee's graph database

        ## Example
        ```json
        {
            "episodes": [
                {
                    "name": "episode_1",
                    "text": "Marie Curie won the Nobel Prize in Physics in 1903.",
                    "reference_time": "1903-12-10T00:00:00"
                }
            ]
        }
        ```
        """
        send_telemetry(
            "Episode Add API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/episodes/add",
                "episodes_count": len(payload.episodes),
                "dataset": payload.dataset,
            },
        )

        try:
            from cognee.tasks.temporal_awareness import build_graph_with_temporal_awareness
            from graphiti_core.nodes import EpisodeType
            
            # Build text list from episodes
            text_list = []
            for episode in payload.episodes:
                text_list.append(episode.text)
            
            # Build graph with temporal awareness using Graphiti
            graphiti = await build_graph_with_temporal_awareness(text_list)
            
            # Add individual episodes with their metadata
            for episode in payload.episodes:
                reference_time = episode.reference_time or datetime.now()
                await graphiti.add_episode(
                    name=episode.name,
                    episode_body=episode.text,
                    source=EpisodeType.text,
                    source_description=episode.source_description,
                    reference_time=reference_time,
                )
            
            # Index the graphiti objects for retrieval
            from cognee.tasks.temporal_awareness.index_graphiti_objects import (
                index_and_transform_graphiti_nodes_and_edges,
            )
            await index_and_transform_graphiti_nodes_and_edges()
            
            await graphiti.close()

            return AddEpisodesResponseDTO(
                message="Episodes added successfully with temporal awareness",
                episodes_added=len(payload.episodes),
                dataset=payload.dataset,
                status="success"
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to add episodes: {str(error)}"}
            )

    @router.post("/search", response_model=SearchEpisodesResponseDTO)
    async def search_episodes(
        payload: SearchEpisodesPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Search episodes with temporal awareness using Graphiti.

        Performs temporal-aware search across episodes, considering both
        semantic similarity and temporal proximity. Results are ranked
        by relevance to the query and temporal context.

        ## Request Parameters
        - **query** (str): Natural language search query
        - **time_from** (Optional[datetime]): Filter episodes after this time
        - **time_to** (Optional[datetime]): Filter episodes before this time
        - **top_k** (int): Maximum number of results (default: 10)

        ## Response
        Returns list of relevant episodes with temporal context.

        ## Features
        - Semantic similarity search
        - Temporal proximity ranking
        - Time-range filtering
        - Context-aware retrieval

        ## Example
        ```json
        {
            "query": "What did Marie Curie accomplish?",
            "time_from": "1900-01-01T00:00:00",
            "time_to": "1910-12-31T23:59:59",
            "top_k": 5
        }
        ```
        """
        send_telemetry(
            "Episode Search API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/episodes/search",
                "query": payload.query,
                "has_time_filter": payload.time_from is not None or payload.time_to is not None,
                "top_k": payload.top_k,
            },
        )

        try:
            from cognee.modules.retrieval.utils.brute_force_triplet_search import (
                brute_force_triplet_search
            )
            
            # Search using vector similarity across graphiti node collections
            triplets = await brute_force_triplet_search(
                query=payload.query,
                top_k=payload.top_k,
                collections=["graphitinode_content", "graphitinode_name", "graphitinode_summary"],
            )
            
            # Convert triplets to episode results
            results = []
            seen_ids = set()
            
            for triplet in triplets:
                # Triplet format: (source_node, edge, target_node, score)
                source_node = triplet[0]
                score = triplet[3] if len(triplet) > 3 else 0.0
                
                # Avoid duplicates
                node_id = source_node.get("id", "")
                if node_id in seen_ids:
                    continue
                seen_ids.add(node_id)
                
                result = EpisodeSearchResultDTO(
                    name=source_node.get("name", "unknown"),
                    content=source_node.get("content", ""),
                    summary=source_node.get("summary"),
                    timestamp=None,  # Graphiti stores timestamps differently
                    relevance_score=float(score)
                )
                results.append(result)
            
            return SearchEpisodesResponseDTO(
                results=results[:payload.top_k],
                query=payload.query,
                total_results=len(results)
            )
            
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Episode search failed: {str(error)}"}
            )

    @router.post("/cognify-with-episodes")
    async def cognify_with_episodes(
        payload: AddEpisodesPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Process episodes using cognify with temporal awareness enabled.

        This endpoint combines episode addition with cognee's cognify pipeline,
        enabling full knowledge graph extraction with temporal context.

        ## Request Parameters
        Same as /add endpoint

        ## Response
        Returns processed episode information

        ## Features
        - Runs cognify with temporal_cognify=True
        - Extracts entities and events from episodes
        - Builds temporal relationships
        - Indexes for semantic search

        ## Example
        ```json
        {
            "episodes": [
                {
                    "name": "historical_event_1",
                    "text": "The Berlin Wall fell on November 9, 1989.",
                    "reference_time": "1989-11-09T00:00:00"
                }
            ],
            "dataset": "historical_events"
        }
        ```
        """
        send_telemetry(
            "Cognify with Episodes API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/episodes/cognify-with-episodes",
                "episodes_count": len(payload.episodes),
                "dataset": payload.dataset,
            },
        )

        try:
            import cognee
            from cognee.api.v1.cognify import cognify
            
            # First add episodes to cognee
            texts = [ep.text for ep in payload.episodes]
            dataset_name = payload.dataset or "episodes"
            
            await cognee.add(texts, dataset_name=dataset_name)
            
            # Run cognify with temporal awareness
            await cognify(
                datasets=[dataset_name],
                user=user,
                temporal_cognify=True
            )
            
            # Also build graphiti graph for enhanced temporal awareness
            from cognee.tasks.temporal_awareness import build_graph_with_temporal_awareness
            from graphiti_core.nodes import EpisodeType
            
            graphiti = await build_graph_with_temporal_awareness(texts)
            
            # Add episodes with metadata
            for episode in payload.episodes:
                reference_time = episode.reference_time or datetime.now()
                await graphiti.add_episode(
                    name=episode.name,
                    episode_body=episode.text,
                    source=EpisodeType.text,
                    source_description=episode.source_description,
                    reference_time=reference_time,
                )
            
            # Index graphiti objects
            from cognee.tasks.temporal_awareness.index_graphiti_objects import (
                index_and_transform_graphiti_nodes_and_edges,
            )
            await index_and_transform_graphiti_nodes_and_edges()
            
            await graphiti.close()

            return {
                "message": "Episodes processed successfully with temporal cognify and graphiti",
                "episodes_added": len(payload.episodes),
                "dataset": dataset_name,
                "status": "success",
                "features": [
                    "temporal_cognify_enabled",
                    "graphiti_temporal_awareness",
                    "entity_extraction",
                    "event_extraction",
                    "temporal_indexing"
                ]
            }
            
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Cognify with episodes failed: {str(error)}"}
            )

    return router
