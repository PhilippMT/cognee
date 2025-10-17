"""
Temporal Search Router

This module provides API endpoints for searching with temporal filters.
"""

from uuid import UUID
from typing import Optional, List
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.modules.search.types import SearchType, SearchResult
from cognee.shared.utils import send_telemetry


class TimestampDTO(BaseModel):
    """Timestamp for temporal queries."""
    year: int = Field(..., ge=1, le=9999, description="Year")
    month: int = Field(1, ge=1, le=12, description="Month (default: 1)")
    day: int = Field(1, ge=1, le=31, description="Day (default: 1)")
    hour: int = Field(0, ge=0, le=23, description="Hour (default: 0)")
    minute: int = Field(0, ge=0, le=59, description="Minute (default: 0)")
    second: int = Field(0, ge=0, le=59, description="Second (default: 0)")


class TemporalSearchPayloadDTO(InDTO):
    """Request payload for temporal search."""
    query: str = Field(..., description="Search query text")
    datasets: Optional[List[str]] = Field(
        default=None,
        description="List of dataset names to search within"
    )
    dataset_ids: Optional[List[UUID]] = Field(
        default=None,
        description="List of dataset UUIDs to search within"
    )
    time_from: Optional[TimestampDTO] = Field(
        default=None,
        description="Start of time range (optional)"
    )
    time_to: Optional[TimestampDTO] = Field(
        default=None,
        description="End of time range (optional)"
    )
    top_k: int = Field(default=10, ge=1, le=100, description="Maximum results to return")


def get_temporal_search_router() -> APIRouter:
    """Create and return the temporal search router."""
    router = APIRouter()

    @router.post("", response_model=List[SearchResult])
    async def temporal_search(
        payload: TemporalSearchPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Search with temporal awareness and optional time range filters.

        This endpoint performs temporal-aware search, automatically extracting
        time information from queries and filtering results by time ranges.

        ## Request Parameters
        - **query** (str): Natural language search query
        - **datasets** (Optional[List[str]]): Dataset names to search within
        - **dataset_ids** (Optional[List[UUID]]): Dataset UUIDs to search within
        - **time_from** (Optional[TimestampDTO]): Start of time range filter
        - **time_to** (Optional[TimestampDTO]): End of time range filter
        - **top_k** (int): Maximum number of results (default: 10)

        ## Response
        Returns a list of search results with temporal context.

        ## Features
        - Automatic time extraction from natural language queries
        - Optional explicit time range filtering
        - Event-based context retrieval
        - Temporal relevance ranking

        ## Example
        ```json
        {
            "query": "What happened during the 1990s?",
            "datasets": ["historical_data"],
            "time_from": {"year": 1990, "month": 1, "day": 1},
            "time_to": {"year": 1999, "month": 12, "day": 31},
            "top_k": 10
        }
        ```
        """
        send_telemetry(
            "Temporal Search API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/temporal/search",
                "query": payload.query,
                "datasets": payload.datasets,
                "dataset_ids": [str(ds_id) for ds_id in payload.dataset_ids or []],
                "has_time_from": payload.time_from is not None,
                "has_time_to": payload.time_to is not None,
                "top_k": payload.top_k,
            },
        )

        from cognee.api.v1.search import search

        try:
            # Perform temporal search
            results = await search(
                query_text=payload.query,
                query_type=SearchType.TEMPORAL,
                user=user,
                datasets=payload.datasets,
                dataset_ids=payload.dataset_ids,
                top_k=payload.top_k,
            )

            return jsonable_encoder(results)
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Temporal search failed: {str(error)}"}
            )

    return router
