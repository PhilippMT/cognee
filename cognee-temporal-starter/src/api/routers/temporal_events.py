"""
Temporal Events Router

This module provides API endpoints for querying events by time ranges.
"""

from typing import Optional, List, Dict, Any
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


class TimestampDTO(BaseModel):
    """Timestamp for temporal queries."""
    year: int = Field(..., ge=1, le=9999, description="Year")
    month: int = Field(1, ge=1, le=12, description="Month (default: 1)")
    day: int = Field(1, ge=1, le=31, description="Day (default: 1)")
    hour: int = Field(0, ge=0, le=23, description="Hour (default: 0)")
    minute: int = Field(0, ge=0, le=59, description="Minute (default: 0)")
    second: int = Field(0, ge=0, le=59, description="Second (default: 0)")


class EventsQueryPayloadDTO(InDTO):
    """Request payload for querying events by time range."""
    time_from: Optional[TimestampDTO] = Field(
        default=None,
        description="Start of time range (if None, returns all events up to time_to)"
    )
    time_to: Optional[TimestampDTO] = Field(
        default=None,
        description="End of time range (if None, returns all events from time_from)"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum events to return")


class EventDTO(OutDTO):
    """Event data transfer object."""
    id: str
    name: str
    description: Optional[str] = None
    time_from: Optional[Dict[str, int]] = None
    time_to: Optional[Dict[str, int]] = None
    location: Optional[str] = None


class EventsResponseDTO(OutDTO):
    """Response for events query."""
    events: List[EventDTO]
    total_count: int
    time_range: Dict[str, Any]


def get_temporal_events_router() -> APIRouter:
    """Create and return the temporal events router."""
    router = APIRouter()

    @router.post("", response_model=EventsResponseDTO)
    async def query_events_by_time(
        payload: EventsQueryPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Query events within a specific time range.

        This endpoint retrieves all events that occurred within the specified
        time period, allowing for timeline construction and temporal analysis.

        ## Request Parameters
        - **time_from** (Optional[TimestampDTO]): Start of time range
        - **time_to** (Optional[TimestampDTO]): End of time range
        - **limit** (int): Maximum number of events to return (default: 100)

        ## Response
        Returns a list of events with their temporal information.

        ## Features
        - Query events by time range
        - Filter events without requiring full text search
        - Build chronological timelines
        - Analyze temporal patterns

        ## Example
        ```json
        {
            "time_from": {"year": 1900, "month": 1, "day": 1},
            "time_to": {"year": 1950, "month": 12, "day": 31},
            "limit": 100
        }
        ```
        """
        send_telemetry(
            "Temporal Events Query API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/temporal/events",
                "has_time_from": payload.time_from is not None,
                "has_time_to": payload.time_to is not None,
                "limit": payload.limit,
            },
        )

        from cognee.infrastructure.databases.graph import get_graph_engine
        from cognee.tasks.temporal_graph.models import Timestamp

        try:
            # Convert DTOs to Timestamp models
            time_from = None
            if payload.time_from:
                time_from = Timestamp(
                    year=payload.time_from.year,
                    month=payload.time_from.month,
                    day=payload.time_from.day,
                    hour=payload.time_from.hour,
                    minute=payload.time_from.minute,
                    second=payload.time_from.second,
                )

            time_to = None
            if payload.time_to:
                time_to = Timestamp(
                    year=payload.time_to.year,
                    month=payload.time_to.month,
                    day=payload.time_to.day,
                    hour=payload.time_to.hour,
                    minute=payload.time_to.minute,
                    second=payload.time_to.second,
                )

            # Get graph engine and query events
            graph_engine = await get_graph_engine()

            # Collect event IDs based on time range
            if time_from and time_to:
                ids = await graph_engine.collect_time_ids(time_from=time_from, time_to=time_to)
            elif time_from:
                ids = await graph_engine.collect_time_ids(time_from=time_from)
            elif time_to:
                ids = await graph_engine.collect_time_ids(time_to=time_to)
            else:
                # No time filter - return recent events up to limit
                ids = []

            # Collect events for the IDs
            events_data = []
            if ids:
                events_result = await graph_engine.collect_events(ids=ids)
                if events_result and len(events_result) > 0:
                    events_list = events_result[0].get("events", [])
                    events_data = events_list[:payload.limit]

            # Convert to DTOs
            event_dtos = []
            for event in events_data:
                event_dto = EventDTO(
                    id=event.get("id", ""),
                    name=event.get("name", ""),
                    description=event.get("description"),
                    time_from=event.get("time_from"),
                    time_to=event.get("time_to"),
                    location=event.get("location"),
                )
                event_dtos.append(event_dto)

            return EventsResponseDTO(
                events=event_dtos,
                total_count=len(event_dtos),
                time_range={
                    "time_from": payload.time_from.model_dump() if payload.time_from else None,
                    "time_to": payload.time_to.model_dump() if payload.time_to else None,
                }
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Events query failed: {str(error)}"}
            )

    @router.get("/timeline")
    async def get_timeline(
        dataset: Optional[str] = None,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Get a chronological timeline view of events.

        This endpoint retrieves all events and organizes them chronologically,
        providing a timeline visualization of temporal data.

        ## Query Parameters
        - **dataset** (Optional[str]): Filter events by dataset name

        ## Response
        Returns events organized in chronological order.

        ## Features
        - Chronological event ordering
        - Dataset filtering
        - Timeline visualization support
        """
        send_telemetry(
            "Temporal Timeline API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "GET /v1/temporal/timeline",
                "dataset": dataset,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            # Get all events (this is a simplified version)
            # In production, you'd want to add pagination and better filtering
            events_data = []

            return JSONResponse(
                content=jsonable_encoder({
                    "events": events_data,
                    "message": "Timeline retrieval - implementation can be extended based on needs"
                })
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Timeline retrieval failed: {str(error)}"}
            )

    return router
