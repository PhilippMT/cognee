"""
Temporal Aware Memory API Server

This server extends the cognee API with temporal-specific endpoints for:
- Temporal cognify operations
- Temporal search with time range filtering
- Event querying by time ranges
- Timeline visualization

It can be run standalone or integrated into the main cognee API server.
"""

import os
import sys

# Add parent cognee to path for imports
cognee_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, cognee_root)

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from cognee.shared.logging_utils import get_logger, setup_logging

# Import cognee API routers
from cognee.api.v1.add.routers import get_add_router
from cognee.api.v1.cognify.routers import get_cognify_router
from cognee.api.v1.search.routers import get_search_router
from cognee.api.v1.datasets.routers import get_datasets_router
from cognee.api.v1.settings.routers import get_settings_router
from cognee.api.v1.users.routers import (
    get_auth_router,
    get_register_router,
    get_users_router,
)

# Import temporal routers
from .routers.temporal_cognify import get_temporal_cognify_router
from .routers.temporal_search import get_temporal_search_router
from .routers.temporal_events import get_temporal_events_router

logger = get_logger()
app_environment = os.getenv("ENV", "local")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Initialize database on startup
    from cognee.infrastructure.databases.relational import get_relational_engine
    from cognee.modules.users.methods import get_default_user

    db_engine = get_relational_engine()
    await db_engine.create_database()
    await get_default_user()

    logger.info("Temporal API server initialized")
    yield
    logger.info("Temporal API server shutting down")


# Create FastAPI app
app = FastAPI(
    title="Cognee Temporal Memory API",
    description="Extended API server with temporal aware memory handling",
    version="1.0.0",
    debug=app_environment != "prod",
    lifespan=lifespan
)

# CORS configuration
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")
if CORS_ALLOWED_ORIGINS:
    allowed_origins = [
        origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",") if origin.strip()
    ]
else:
    allowed_origins = [
        os.getenv("UI_APP_URL", "http://localhost:3000"),
        "http://localhost:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Cognee Temporal Memory API",
        "version": "1.0.0",
        "endpoints": {
            "temporal_cognify": "/api/v1/temporal/cognify",
            "temporal_search": "/api/v1/temporal/search",
            "temporal_events": "/api/v1/temporal/events",
            "timeline": "/api/v1/temporal/timeline",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "temporal-api"}
    )


# Include standard cognee API routers
app.include_router(get_auth_router(), prefix="/api/v1/auth", tags=["auth"])
app.include_router(get_register_router(), prefix="/api/v1/auth", tags=["auth"])
app.include_router(get_users_router(), prefix="/api/v1/users", tags=["users"])
app.include_router(get_add_router(), prefix="/api/v1/add", tags=["add"])
app.include_router(get_cognify_router(), prefix="/api/v1/cognify", tags=["cognify"])
app.include_router(get_search_router(), prefix="/api/v1/search", tags=["search"])
app.include_router(get_datasets_router(), prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(get_settings_router(), prefix="/api/v1/settings", tags=["settings"])

# Include temporal-specific routers
app.include_router(
    get_temporal_cognify_router(),
    prefix="/api/v1/temporal/cognify",
    tags=["temporal"]
)
app.include_router(
    get_temporal_search_router(),
    prefix="/api/v1/temporal/search",
    tags=["temporal"]
)
app.include_router(
    get_temporal_events_router(),
    prefix="/api/v1/temporal/events",
    tags=["temporal"]
)


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Start the temporal API server.
    
    Args:
        host: Host to bind the server to (default: 0.0.0.0)
        port: Port to bind the server to (default: 8000)
    """
    setup_logging()
    logger.info(f"Starting Temporal API server on {host}:{port}")
    
    uvicorn.run(
        "temporal_server:app",
        host=host,
        port=port,
        reload=app_environment == "local",
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
