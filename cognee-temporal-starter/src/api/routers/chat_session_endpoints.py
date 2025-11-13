"""
Coding Agent Chat Session - API Endpoints

This module provides REST API endpoints for processing and querying
coding agent chat sessions with temporal awareness.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


# Request/Response Models

class ChatMessageDTO(BaseModel):
    """DTO for a chat message."""
    role: str = Field(..., description="user, assistant, agent, tool, system")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO format timestamp")
    message_id: Optional[str] = Field(None, description="Optional message ID")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(None, description="Tool calls made")


class IngestChatSessionPayloadDTO(InDTO):
    """Request payload for ingesting a chat session."""
    session_id: Optional[str] = Field(None, description="Optional session ID")
    messages: List[ChatMessageDTO] = Field(..., description="List of chat messages")
    use_graphiti: bool = Field(default=True, description="Use Graphiti for temporal awareness")
    extract_deep_facts: bool = Field(default=True, description="Perform deep fact extraction")
    preserve_raw_data: bool = Field(default=True, description="Store raw messages")


class IngestChatSessionResponseDTO(OutDTO):
    """Response for chat session ingestion."""
    session_id: str
    messages_processed: int
    facts_extracted: int
    decisions_found: int
    code_entities: int
    processing_time: float
    status: str


class SearchSessionsPayloadDTO(InDTO):
    """Request payload for searching chat sessions."""
    query: str = Field(..., description="Search query")
    session_ids: Optional[List[str]] = Field(None, description="Filter by session IDs")
    session_types: Optional[List[str]] = Field(None, description="Filter by session types")
    date_from: Optional[str] = Field(None, description="Filter by start date (ISO format)")
    date_to: Optional[str] = Field(None, description="Filter by end date (ISO format)")
    fact_types: Optional[List[str]] = Field(None, description="Filter by fact types")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results")


class SessionSummaryDTO(BaseModel):
    """Summary of a chat session."""
    session_id: str
    session_type: str
    session_goal: str
    start_time: str
    end_time: Optional[str]
    message_count: int
    facts_count: int
    decisions_count: int
    code_changes: List[str]


class SearchSessionsResponseDTO(OutDTO):
    """Response for session search."""
    query: str
    sessions: List[SessionSummaryDTO]
    total_sessions: int


class TimelineEventDTO(BaseModel):
    """Timeline event."""
    timestamp: str
    event_type: str
    description: str
    message_id: Optional[str]
    entities: List[str]


class GetTimelineResponseDTO(OutDTO):
    """Response for timeline retrieval."""
    session_id: str
    timeline: List[TimelineEventDTO]
    milestones: List[Dict[str, Any]]
    blockers: List[Dict[str, Any]]


class FactDTO(BaseModel):
    """Development fact."""
    fact_type: str
    description: str
    status: str
    valid_at: str
    invalid_at: Optional[str]
    confidence: float
    related_messages: List[str]
    entities: List[str]


class GetFactsResponseDTO(OutDTO):
    """Response for facts retrieval."""
    session_id: str
    facts: List[FactDTO]
    total_facts: int


class PatternDTO(BaseModel):
    """Interaction pattern."""
    pattern_type: str
    description: str
    frequency: int
    effectiveness: Optional[float]
    sessions: List[str]


class GetPatternsResponseDTO(OutDTO):
    """Response for patterns retrieval."""
    patterns: List[PatternDTO]
    total_patterns: int


def get_chat_session_router() -> APIRouter:
    """Create and return the chat session router."""
    router = APIRouter()

    @router.post("/ingest", response_model=IngestChatSessionResponseDTO)
    async def ingest_chat_session(
        payload: IngestChatSessionPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Ingest and process a coding agent chat session.

        This endpoint processes chat sessions with temporal awareness using Graphiti
        and Cognee's temporal graph capabilities.

        ## Features
        - Temporal episode creation
        - Event extraction
        - Fact mining
        - Decision tracking
        - Code entity identification
        - Timeline construction

        ## Request Body
        ```json
        {
            "session_id": "optional_session_id",
            "messages": [
                {
                    "role": "user",
                    "content": "Implement authentication",
                    "timestamp": "2024-01-15T10:00:00Z"
                }
            ],
            "use_graphiti": true,
            "extract_deep_facts": true
        }
        ```

        ## Response
        ```json
        {
            "session_id": "auth_impl_001",
            "messages_processed": 15,
            "facts_extracted": 8,
            "decisions_found": 3,
            "code_entities": 5,
            "processing_time": 12.5,
            "status": "completed"
        }
        ```
        """
        send_telemetry(
            "Ingest Chat Session API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/chat-sessions/ingest",
                "messages_count": len(payload.messages),
            },
        )

        try:
            from cognee_temporal_starter.src.pipelines.chat_session_processor import process_coding_session
            
            # Convert DTOs to dicts
            chat_history = [msg.dict() for msg in payload.messages]
            
            # Process the session
            results = await process_coding_session(
                chat_history=chat_history,
                session_id=payload.session_id,
                use_graphiti=payload.use_graphiti,
                extract_deep_facts=payload.extract_deep_facts,
                preserve_raw_data=payload.preserve_raw_data
            )
            
            return IngestChatSessionResponseDTO(**results)
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to process chat session: {str(error)}"}
            )

    @router.post("/search", response_model=SearchSessionsResponseDTO)
    async def search_sessions(
        payload: SearchSessionsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Search across processed chat sessions.

        Find sessions, facts, or insights based on queries with temporal filtering.

        ## Request Body
        ```json
        {
            "query": "authentication implementation",
            "session_types": ["feature_development"],
            "date_from": "2024-01-01T00:00:00Z",
            "top_k": 10
        }
        ```
        """
        send_telemetry(
            "Search Chat Sessions API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/chat-sessions/search",
                "query": payload.query,
            },
        )

        try:
            from cognee.api.v1.search import search, SearchType
            
            # Search using temporal awareness
            results = await search(
                query_text=payload.query,
                query_type=SearchType.TEMPORAL,
                limit=payload.top_k
            )
            
            # Transform results to session summaries
            # (Simplified - would need proper parsing)
            sessions = []
            
            return SearchSessionsResponseDTO(
                query=payload.query,
                sessions=sessions,
                total_sessions=len(sessions)
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to search sessions: {str(error)}"}
            )

    @router.get("/{session_id}/timeline", response_model=GetTimelineResponseDTO)
    async def get_timeline(
        session_id: str,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get the timeline of events for a specific session.

        Returns chronological view of development activities including:
        - Code changes
        - Decisions made
        - Tool usage
        - Milestones achieved
        - Blockers encountered

        ## Example Response
        ```json
        {
            "session_id": "auth_impl_001",
            "timeline": [
                {
                    "timestamp": "2024-01-15T10:00:00Z",
                    "event_type": "session_start",
                    "description": "User requested authentication implementation"
                }
            ],
            "milestones": [],
            "blockers": []
        }
        ```
        """
        send_telemetry(
            "Get Timeline API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": f"GET /v1/chat-sessions/{session_id}/timeline",
            },
        )

        try:
            # Would retrieve timeline from stored data
            timeline = []
            milestones = []
            blockers = []
            
            return GetTimelineResponseDTO(
                session_id=session_id,
                timeline=timeline,
                milestones=milestones,
                blockers=blockers
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get timeline: {str(error)}"}
            )

    @router.get("/{session_id}/facts", response_model=GetFactsResponseDTO)
    async def get_facts(
        session_id: str,
        fact_types: Optional[List[str]] = None,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get extracted facts for a specific session.

        Returns development facts including:
        - Code changes
        - Bug fixes
        - Feature additions
        - Refactorings
        - Dependencies

        ## Query Parameters
        - fact_types: Filter by fact types (code_change, bug_fix, feature, etc.)

        ## Example Response
        ```json
        {
            "session_id": "auth_impl_001",
            "facts": [
                {
                    "fact_type": "feature",
                    "description": "Implemented JWT authentication",
                    "status": "completed",
                    "confidence": 0.95
                }
            ],
            "total_facts": 1
        }
        ```
        """
        send_telemetry(
            "Get Facts API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": f"GET /v1/chat-sessions/{session_id}/facts",
            },
        )

        try:
            # Would retrieve facts from stored data
            facts = []
            
            return GetFactsResponseDTO(
                session_id=session_id,
                facts=facts,
                total_facts=len(facts)
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get facts: {str(error)}"}
            )

    @router.get("/patterns", response_model=GetPatternsResponseDTO)
    async def get_patterns(
        pattern_types: Optional[List[str]] = None,
        min_frequency: int = 2,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get recurring patterns across all chat sessions.

        Identifies patterns like:
        - Question-answer sequences
        - Error resolution flows
        - Decision-making processes
        - Common clarifications

        ## Query Parameters
        - pattern_types: Filter by pattern types
        - min_frequency: Minimum occurrence count

        ## Example Response
        ```json
        {
            "patterns": [
                {
                    "pattern_type": "error_resolution",
                    "description": "Security issue detected and fixed",
                    "frequency": 5,
                    "effectiveness": 0.9
                }
            ],
            "total_patterns": 1
        }
        ```
        """
        send_telemetry(
            "Get Patterns API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "GET /v1/chat-sessions/patterns",
            },
        )

        try:
            # Would retrieve patterns from analysis
            patterns = []
            
            return GetPatternsResponseDTO(
                patterns=patterns,
                total_patterns=len(patterns)
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to get patterns: {str(error)}"}
            )

    return router
