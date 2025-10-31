"""
Advanced Event Relationship Tracking API

This module provides endpoints for tracking and querying advanced relationships
between events, including causality, parent/child hierarchies, and temporal chains.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


class RelationshipType(BaseModel):
    """Type of relationship between events."""
    name: str = Field(..., description="Relationship type name")
    description: Optional[str] = Field(None, description="Description of the relationship")


class CausalRelationship(BaseModel):
    """Causal relationship between events."""
    cause_event: str = Field(..., description="Name or ID of the causing event")
    effect_event: str = Field(..., description="Name or ID of the effect event")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in the causal link")
    evidence: Optional[str] = Field(None, description="Evidence for the causal relationship")


class HierarchicalRelationship(BaseModel):
    """Parent-child relationship between events."""
    parent_event: str = Field(..., description="Name or ID of the parent event")
    child_event: str = Field(..., description="Name or ID of the child event")
    hierarchy_type: str = Field(default="contains", description="Type of hierarchy (contains, part_of, etc.)")


class AddRelationshipsPayloadDTO(InDTO):
    """Request payload for adding event relationships."""
    causal_relationships: List[CausalRelationship] = Field(
        default=[],
        description="Causal relationships to add"
    )
    hierarchical_relationships: List[HierarchicalRelationship] = Field(
        default=[],
        description="Hierarchical relationships to add"
    )
    dataset: Optional[str] = Field(None, description="Dataset to scope relationships to")


class AddRelationshipsResponseDTO(OutDTO):
    """Response for adding relationships."""
    message: str
    causal_added: int
    hierarchical_added: int
    status: str


class QueryRelationshipsPayloadDTO(InDTO):
    """Request payload for querying relationships."""
    event_name: str = Field(..., description="Event to query relationships for")
    relationship_types: List[str] = Field(
        default=["causal", "hierarchical"],
        description="Types of relationships to query"
    )
    direction: str = Field(
        default="both",
        description="Direction to traverse (incoming, outgoing, both)"
    )
    max_depth: int = Field(default=2, ge=1, le=10, description="Maximum depth to traverse")


class EventRelationshipDTO(OutDTO):
    """Event relationship data."""
    from_event: str
    to_event: str
    relationship_type: str
    properties: Dict[str, Any]


class QueryRelationshipsResponseDTO(OutDTO):
    """Response for relationship queries."""
    event_name: str
    relationships: List[EventRelationshipDTO]
    total_count: int


class CausalChainPayloadDTO(InDTO):
    """Request payload for finding causal chains."""
    start_event: str = Field(..., description="Starting event")
    end_event: Optional[str] = Field(None, description="Target end event (optional)")
    max_chain_length: int = Field(default=5, ge=2, le=20, description="Maximum chain length")


class CausalChainDTO(OutDTO):
    """A causal chain of events."""
    chain: List[str]
    confidence: float
    length: int


class CausalChainResponseDTO(OutDTO):
    """Response for causal chain queries."""
    start_event: str
    end_event: Optional[str]
    chains: List[CausalChainDTO]
    total_chains: int


def get_relationship_tracking_router() -> APIRouter:
    """Create and return the relationship tracking router."""
    router = APIRouter()

    @router.post("/add", response_model=AddRelationshipsResponseDTO)
    async def add_relationships(
        payload: AddRelationshipsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Add advanced relationships between events.

        This endpoint allows explicit definition of causal and hierarchical
        relationships between events in the temporal graph.

        ## Request Parameters
        - **causal_relationships**: List of cause-effect relationships
        - **hierarchical_relationships**: List of parent-child relationships
        - **dataset**: Optional dataset to scope relationships to

        ## Features
        - Explicit causality tracking
        - Parent-child event hierarchies
        - Confidence scoring for relationships
        - Evidence linking

        ## Example
        ```json
        {
            "causal_relationships": [
                {
                    "cause_event": "stock_market_crash_1929",
                    "effect_event": "great_depression",
                    "confidence": 0.95,
                    "evidence": "Economic historians agree..."
                }
            ],
            "hierarchical_relationships": [
                {
                    "parent_event": "world_war_ii",
                    "child_event": "battle_of_normandy",
                    "hierarchy_type": "contains"
                }
            ]
        }
        ```
        """
        send_telemetry(
            "Add Relationships API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/relationships/add",
                "causal_count": len(payload.causal_relationships),
                "hierarchical_count": len(payload.hierarchical_relationships),
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine
            from cognee.infrastructure.engine.models import Edge

            graph_engine = await get_graph_engine()
            
            causal_added = 0
            hierarchical_added = 0
            
            # Add causal relationships
            for causal in payload.causal_relationships:
                # Find event nodes
                cause_nodes = await graph_engine.query(
                    "MATCH (e) WHERE e.name = $event_name RETURN e",
                    params={"event_name": causal.cause_event}
                )
                effect_nodes = await graph_engine.query(
                    "MATCH (e) WHERE e.name = $event_name RETURN e",
                    params={"event_name": causal.effect_event}
                )
                
                if cause_nodes and effect_nodes:
                    # Create causal edge
                    edge_properties = {
                        "relationship_type": "CAUSES",
                        "confidence": causal.confidence,
                        "evidence": causal.evidence or ""
                    }
                    
                    # Add edge between events
                    await graph_engine.query(
                        """MATCH (cause) WHERE cause.name = $cause_name
                           MATCH (effect) WHERE effect.name = $effect_name
                           CREATE (cause)-[r:CAUSES {confidence: $confidence, evidence: $evidence}]->(effect)
                           RETURN r""",
                        params={
                            "cause_name": causal.cause_event,
                            "effect_name": causal.effect_event,
                            "confidence": causal.confidence,
                            "evidence": causal.evidence or ""
                        }
                    )
                    causal_added += 1
            
            # Add hierarchical relationships
            for hierarchy in payload.hierarchical_relationships:
                parent_nodes = await graph_engine.query(
                    "MATCH (e) WHERE e.name = $event_name RETURN e",
                    params={"event_name": hierarchy.parent_event}
                )
                child_nodes = await graph_engine.query(
                    "MATCH (e) WHERE e.name = $event_name RETURN e",
                    params={"event_name": hierarchy.child_event}
                )
                
                if parent_nodes and child_nodes:
                    relationship_label = hierarchy.hierarchy_type.upper()
                    
                    await graph_engine.query(
                        f"""MATCH (parent) WHERE parent.name = $parent_name
                           MATCH (child) WHERE child.name = $child_name
                           CREATE (parent)-[r:{relationship_label}]->(child)
                           RETURN r""",
                        params={
                            "parent_name": hierarchy.parent_event,
                            "child_name": hierarchy.child_event
                        }
                    )
                    hierarchical_added += 1

            return AddRelationshipsResponseDTO(
                message="Relationships added successfully",
                causal_added=causal_added,
                hierarchical_added=hierarchical_added,
                status="success"
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to add relationships: {str(error)}"}
            )

    @router.post("/query", response_model=QueryRelationshipsResponseDTO)
    async def query_relationships(
        payload: QueryRelationshipsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Query relationships for a specific event.

        Retrieve all relationships connected to an event, including causal
        and hierarchical connections.

        ## Request Parameters
        - **event_name**: Event to query relationships for
        - **relationship_types**: Types to include (causal, hierarchical)
        - **direction**: Traverse incoming, outgoing, or both
        - **max_depth**: How many hops to traverse

        ## Example
        ```json
        {
            "event_name": "world_war_ii",
            "relationship_types": ["causal", "hierarchical"],
            "direction": "both",
            "max_depth": 2
        }
        ```
        """
        send_telemetry(
            "Query Relationships API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/relationships/query",
                "event_name": payload.event_name,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            relationships = []
            
            # Query based on direction
            if payload.direction in ["outgoing", "both"]:
                # Get outgoing relationships
                outgoing = await graph_engine.query(
                    """MATCH (e)-[r]->(target)
                       WHERE e.name = $event_name
                       RETURN e.name as from_event, target.name as to_event, 
                              type(r) as rel_type, properties(r) as props
                       LIMIT 100""",
                    params={"event_name": payload.event_name}
                )
                
                for rel in outgoing:
                    relationships.append(EventRelationshipDTO(
                        from_event=rel.get("from_event", ""),
                        to_event=rel.get("to_event", ""),
                        relationship_type=rel.get("rel_type", ""),
                        properties=rel.get("props", {})
                    ))
            
            if payload.direction in ["incoming", "both"]:
                # Get incoming relationships
                incoming = await graph_engine.query(
                    """MATCH (source)-[r]->(e)
                       WHERE e.name = $event_name
                       RETURN source.name as from_event, e.name as to_event,
                              type(r) as rel_type, properties(r) as props
                       LIMIT 100""",
                    params={"event_name": payload.event_name}
                )
                
                for rel in incoming:
                    relationships.append(EventRelationshipDTO(
                        from_event=rel.get("from_event", ""),
                        to_event=rel.get("to_event", ""),
                        relationship_type=rel.get("rel_type", ""),
                        properties=rel.get("props", {})
                    ))

            return QueryRelationshipsResponseDTO(
                event_name=payload.event_name,
                relationships=relationships,
                total_count=len(relationships)
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to query relationships: {str(error)}"}
            )

    @router.post("/causal-chains", response_model=CausalChainResponseDTO)
    async def find_causal_chains(
        payload: CausalChainPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Find causal chains between events.

        Discover sequences of cause-effect relationships, useful for
        understanding how events influence each other over time.

        ## Request Parameters
        - **start_event**: Starting point of the chain
        - **end_event**: Optional target endpoint
        - **max_chain_length**: Maximum length of chains to find

        ## Features
        - Multi-hop causality tracking
        - Confidence propagation through chains
        - Path finding between events

        ## Example
        ```json
        {
            "start_event": "assassination_archduke_ferdinand",
            "end_event": "world_war_ii",
            "max_chain_length": 5
        }
        ```
        """
        send_telemetry(
            "Find Causal Chains API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/relationships/causal-chains",
                "start_event": payload.start_event,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            chains = []
            
            if payload.end_event:
                # Find paths between start and end
                result = await graph_engine.query(
                    """MATCH path = (start)-[:CAUSES*1..{max_length}]->(end)
                       WHERE start.name = $start_name AND end.name = $end_name
                       RETURN [node in nodes(path) | node.name] as chain,
                              [rel in relationships(path) | rel.confidence] as confidences
                       LIMIT 10""".replace("{max_length}", str(payload.max_chain_length)),
                    params={
                        "start_name": payload.start_event,
                        "end_name": payload.end_event
                    }
                )
            else:
                # Find all causal chains from start
                result = await graph_engine.query(
                    """MATCH path = (start)-[:CAUSES*1..{max_length}]->(end)
                       WHERE start.name = $start_name
                       RETURN [node in nodes(path) | node.name] as chain,
                              [rel in relationships(path) | rel.confidence] as confidences
                       LIMIT 10""".replace("{max_length}", str(payload.max_chain_length)),
                    params={"start_name": payload.start_event}
                )
            
            for row in result:
                chain_nodes = row.get("chain", [])
                confidences = row.get("confidences", [])
                
                # Calculate overall confidence (product of individual confidences)
                overall_confidence = 1.0
                for conf in confidences:
                    if conf is not None:
                        overall_confidence *= float(conf)
                
                chains.append(CausalChainDTO(
                    chain=chain_nodes,
                    confidence=overall_confidence,
                    length=len(chain_nodes)
                ))

            return CausalChainResponseDTO(
                start_event=payload.start_event,
                end_event=payload.end_event,
                chains=chains,
                total_chains=len(chains)
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to find causal chains: {str(error)}"}
            )

    return router
