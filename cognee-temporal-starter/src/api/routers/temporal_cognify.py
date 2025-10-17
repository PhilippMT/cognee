"""
Temporal Cognify Router

This module provides API endpoints for running cognify with temporal awareness enabled.
"""

from uuid import UUID
from typing import Optional, List
from pydantic import Field
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


class TemporalCognifyPayloadDTO(InDTO):
    """Request payload for temporal cognify operation."""
    datasets: Optional[List[str]] = Field(
        default=None,
        description="List of dataset names to process with temporal cognify"
    )
    dataset_ids: Optional[List[UUID]] = Field(
        default=None,
        description="List of dataset UUIDs to process"
    )


class TemporalCognifyResponseDTO(OutDTO):
    """Response for temporal cognify operation."""
    message: str
    datasets_processed: List[str]
    status: str


def get_temporal_cognify_router() -> APIRouter:
    """Create and return the temporal cognify router."""
    router = APIRouter()

    @router.post("", response_model=TemporalCognifyResponseDTO)
    async def temporal_cognify(
        payload: TemporalCognifyPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Run cognify with temporal awareness enabled.

        This endpoint processes datasets with temporal event extraction enabled,
        allowing for time-based queries and event timeline construction.

        ## Request Parameters
        - **datasets** (Optional[List[str]]): List of dataset names to process
        - **dataset_ids** (Optional[List[UUID]]): List of dataset UUIDs to process

        ## Response
        Returns information about the processed datasets and status.

        ## Features
        - Extracts events and their timestamps from text
        - Creates temporal relationships between entities
        - Enables time-range based queries
        - Builds event timelines

        ## Example
        ```json
        {
            "datasets": ["historical_documents", "biographies"]
        }
        ```
        """
        send_telemetry(
            "Temporal Cognify API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/temporal/cognify",
                "datasets": payload.datasets,
                "dataset_ids": [str(ds_id) for ds_id in payload.dataset_ids or []],
            },
        )

        from cognee.api.v1.cognify import cognify

        try:
            # Run cognify with temporal awareness enabled
            await cognify(
                datasets=payload.datasets or payload.dataset_ids,
                user=user,
                temporal_cognify=True  # Enable temporal processing
            )

            return TemporalCognifyResponseDTO(
                message="Temporal cognify completed successfully",
                datasets_processed=payload.datasets or [str(ds_id) for ds_id in payload.dataset_ids or []],
                status="success"
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Temporal cognify failed: {str(error)}"}
            )

    return router
