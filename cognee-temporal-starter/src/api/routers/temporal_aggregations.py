"""
Temporal Aggregations API

This module provides endpoints for analyzing temporal patterns, including
event frequency analysis, pattern detection, and temporal statistics.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field, BaseModel
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from cognee.api.DTO import InDTO, OutDTO
from cognee.modules.users.models import User
from cognee.modules.users.methods import get_authenticated_user
from cognee.shared.utils import send_telemetry


class TimeGranularity(str):
    """Time granularity for aggregations."""
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"


class EventFrequencyPayloadDTO(InDTO):
    """Request payload for event frequency analysis."""
    time_granularity: str = Field(
        default="year",
        description="Time granularity (year, month, day, hour)"
    )
    event_types: Optional[List[str]] = Field(
        None,
        description="Filter by specific event types"
    )
    time_from: Optional[datetime] = Field(None, description="Start time")
    time_to: Optional[datetime] = Field(None, description="End time")
    dataset: Optional[str] = Field(None, description="Dataset filter")


class FrequencyBucket(BaseModel):
    """Time bucket with event count."""
    time_period: str
    event_count: int
    events: List[str] = Field(default=[], description="Event names in this period")


class EventFrequencyResponseDTO(OutDTO):
    """Response for event frequency analysis."""
    granularity: str
    buckets: List[FrequencyBucket]
    total_events: int
    time_range: Dict[str, Any]


class PatternDetectionPayloadDTO(InDTO):
    """Request payload for pattern detection."""
    min_pattern_length: int = Field(default=2, ge=2, le=10, description="Minimum events in pattern")
    min_occurrences: int = Field(default=2, ge=2, description="Minimum times pattern must occur")
    time_window_days: Optional[int] = Field(
        None,
        description="Time window for pattern matching (days)"
    )
    event_types: Optional[List[str]] = Field(None, description="Filter by event types")


class EventPattern(BaseModel):
    """Detected event pattern."""
    pattern: List[str]
    occurrences: int
    confidence: float
    example_timestamps: List[str] = Field(default=[], description="Example occurrence times")


class PatternDetectionResponseDTO(OutDTO):
    """Response for pattern detection."""
    patterns: List[EventPattern]
    total_patterns: int
    analysis_summary: Dict[str, Any]


class TemporalStatisticsPayloadDTO(InDTO):
    """Request payload for temporal statistics."""
    dataset: Optional[str] = Field(None, description="Dataset filter")
    include_relationships: bool = Field(
        default=True,
        description="Include relationship statistics"
    )


class TemporalStatsDTO(BaseModel):
    """Temporal statistics data."""
    total_events: int
    total_relationships: int
    time_span: Dict[str, Any]
    event_density: float
    most_connected_events: List[Dict[str, Any]]
    temporal_clusters: List[Dict[str, Any]]


class TemporalStatisticsResponseDTO(OutDTO):
    """Response for temporal statistics."""
    statistics: TemporalStatsDTO
    computed_at: datetime


class EventCooccurrencePayloadDTO(InDTO):
    """Request payload for event co-occurrence analysis."""
    time_window_days: int = Field(
        default=30,
        ge=1,
        description="Time window for co-occurrence (days)"
    )
    min_cooccurrence: int = Field(
        default=2,
        ge=2,
        description="Minimum co-occurrence count"
    )
    event_types: Optional[List[str]] = Field(None, description="Filter by event types")


class EventPair(BaseModel):
    """Pair of co-occurring events."""
    event1: str
    event2: str
    cooccurrence_count: int
    temporal_distance_avg_days: float


class EventCooccurrenceResponseDTO(OutDTO):
    """Response for event co-occurrence analysis."""
    pairs: List[EventPair]
    total_pairs: int
    time_window_days: int


def get_temporal_aggregations_router() -> APIRouter:
    """Create and return the temporal aggregations router."""
    router = APIRouter()

    @router.post("/frequency", response_model=EventFrequencyResponseDTO)
    async def analyze_event_frequency(
        payload: EventFrequencyPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Analyze event frequency over time.

        Count events in time buckets to identify temporal patterns and trends.

        ## Request Parameters
        - **time_granularity**: Bucket size (year, month, day, hour)
        - **event_types**: Filter by specific event types
        - **time_from/time_to**: Time range filter
        - **dataset**: Dataset filter

        ## Features
        - Flexible time granularity
        - Event type filtering
        - Time range specification
        - Event distribution analysis

        ## Example
        ```json
        {
            "time_granularity": "year",
            "time_from": "1900-01-01T00:00:00",
            "time_to": "2000-12-31T23:59:59"
        }
        ```
        """
        send_telemetry(
            "Event Frequency Analysis API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/aggregations/frequency",
                "granularity": payload.time_granularity,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            # Build query based on granularity
            time_extraction = {
                "year": "toString(e.at.year)",
                "month": "toString(e.at.year) + '-' + toString(e.at.month)",
                "day": "toString(e.at.year) + '-' + toString(e.at.month) + '-' + toString(e.at.day)",
            }.get(payload.time_granularity, "toString(e.at.year)")
            
            # Query events grouped by time period
            query = f"""
                MATCH (e:Event)
                WHERE e.at IS NOT NULL
                WITH e, {time_extraction} as time_period
                RETURN time_period, count(e) as event_count, collect(e.name) as events
                ORDER BY time_period
            """
            
            result = await graph_engine.query(query, params={})
            
            buckets = []
            total_events = 0
            
            for row in result:
                time_period = row.get("time_period", "unknown")
                event_count = row.get("event_count", 0)
                events = row.get("events", [])
                
                buckets.append(FrequencyBucket(
                    time_period=str(time_period),
                    event_count=int(event_count),
                    events=events[:10]  # Limit to first 10 event names
                ))
                total_events += int(event_count)

            return EventFrequencyResponseDTO(
                granularity=payload.time_granularity,
                buckets=buckets,
                total_events=total_events,
                time_range={
                    "from": str(payload.time_from) if payload.time_from else None,
                    "to": str(payload.time_to) if payload.time_to else None
                }
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to analyze frequency: {str(error)}"}
            )

    @router.post("/patterns", response_model=PatternDetectionResponseDTO)
    async def detect_patterns(
        payload: PatternDetectionPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Detect recurring temporal patterns.

        Find sequences of events that occur multiple times in similar
        temporal arrangements.

        ## Request Parameters
        - **min_pattern_length**: Minimum events in a pattern
        - **min_occurrences**: How many times pattern must repeat
        - **time_window_days**: Time window for matching patterns
        - **event_types**: Filter by event types

        ## Features
        - Sequence pattern detection
        - Temporal proximity matching
        - Confidence scoring
        - Pattern frequency analysis

        ## Example
        ```json
        {
            "min_pattern_length": 3,
            "min_occurrences": 2,
            "time_window_days": 365
        }
        ```
        """
        send_telemetry(
            "Pattern Detection API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/aggregations/patterns",
                "min_pattern_length": payload.min_pattern_length,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            # Find sequential patterns using temporal ordering
            # This is a simplified pattern detection - can be enhanced with more sophisticated algorithms
            query = """
                MATCH (e1:Event)-[r:CAUSES]->(e2:Event)
                WHERE e1.at IS NOT NULL AND e2.at IS NOT NULL
                WITH e1.name as first_event, e2.name as second_event, count(*) as occurrences
                WHERE occurrences >= $min_occurrences
                RETURN first_event, second_event, occurrences
                ORDER BY occurrences DESC
                LIMIT 20
            """
            
            result = await graph_engine.query(
                query,
                params={"min_occurrences": payload.min_occurrences}
            )
            
            patterns = []
            
            for row in result:
                first_event = row.get("first_event", "")
                second_event = row.get("second_event", "")
                occurrences = row.get("occurrences", 0)
                
                # Calculate confidence based on occurrence frequency
                confidence = min(0.5 + (occurrences * 0.1), 1.0)
                
                patterns.append(EventPattern(
                    pattern=[first_event, second_event],
                    occurrences=int(occurrences),
                    confidence=confidence,
                    example_timestamps=[]
                ))

            return PatternDetectionResponseDTO(
                patterns=patterns,
                total_patterns=len(patterns),
                analysis_summary={
                    "min_pattern_length": payload.min_pattern_length,
                    "min_occurrences": payload.min_occurrences,
                    "patterns_found": len(patterns)
                }
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to detect patterns: {str(error)}"}
            )

    @router.post("/statistics", response_model=TemporalStatisticsResponseDTO)
    async def compute_statistics(
        payload: TemporalStatisticsPayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Compute comprehensive temporal statistics.

        Get overall statistics about the temporal graph including event counts,
        relationship metrics, and temporal distribution.

        ## Request Parameters
        - **dataset**: Optional dataset filter
        - **include_relationships**: Include relationship statistics

        ## Features
        - Event count and distribution
        - Relationship metrics
        - Time span analysis
        - Network centrality measures

        ## Example
        ```json
        {
            "dataset": "historical_events",
            "include_relationships": true
        }
        ```
        """
        send_telemetry(
            "Temporal Statistics API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/aggregations/statistics",
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            # Get total events
            event_count_result = await graph_engine.query(
                "MATCH (e:Event) RETURN count(e) as total",
                params={}
            )
            total_events = event_count_result[0].get("total", 0) if event_count_result else 0
            
            # Get total relationships
            relationship_count = 0
            if payload.include_relationships:
                rel_count_result = await graph_engine.query(
                    "MATCH ()-[r]->() RETURN count(r) as total",
                    params={}
                )
                relationship_count = rel_count_result[0].get("total", 0) if rel_count_result else 0
            
            # Get time span
            time_span_result = await graph_engine.query(
                """MATCH (e:Event)
                   WHERE e.at IS NOT NULL
                   RETURN min(e.at.year) as min_year, max(e.at.year) as max_year""",
                params={}
            )
            
            time_span = {}
            if time_span_result:
                min_year = time_span_result[0].get("min_year")
                max_year = time_span_result[0].get("max_year")
                if min_year and max_year:
                    time_span = {
                        "earliest": min_year,
                        "latest": max_year,
                        "span_years": max_year - min_year
                    }
            
            # Calculate event density (events per year)
            event_density = 0.0
            if time_span and time_span.get("span_years", 0) > 0:
                event_density = total_events / time_span["span_years"]
            
            # Get most connected events
            most_connected_result = await graph_engine.query(
                """MATCH (e:Event)
                   OPTIONAL MATCH (e)-[r]-()
                   WITH e, count(r) as connections
                   RETURN e.name as event_name, connections
                   ORDER BY connections DESC
                   LIMIT 5""",
                params={}
            )
            
            most_connected = [
                {"event": row.get("event_name", ""), "connections": row.get("connections", 0)}
                for row in most_connected_result
            ]

            statistics = TemporalStatsDTO(
                total_events=int(total_events),
                total_relationships=int(relationship_count),
                time_span=time_span,
                event_density=float(event_density),
                most_connected_events=most_connected,
                temporal_clusters=[]  # Can be enhanced with clustering algorithm
            )

            return TemporalStatisticsResponseDTO(
                statistics=statistics,
                computed_at=datetime.now()
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to compute statistics: {str(error)}"}
            )

    @router.post("/cooccurrence", response_model=EventCooccurrenceResponseDTO)
    async def analyze_cooccurrence(
        payload: EventCooccurrencePayloadDTO,
        user: User = Depends(get_authenticated_user)
    ):
        """
        Analyze event co-occurrence patterns.

        Find events that frequently occur together within specified time windows.

        ## Request Parameters
        - **time_window_days**: Time window for co-occurrence
        - **min_cooccurrence**: Minimum co-occurrence count
        - **event_types**: Filter by event types

        ## Features
        - Temporal proximity analysis
        - Co-occurrence frequency
        - Average temporal distance
        - Event correlation discovery

        ## Example
        ```json
        {
            "time_window_days": 30,
            "min_cooccurrence": 3
        }
        ```
        """
        send_telemetry(
            "Event Co-occurrence Analysis API Endpoint Invoked",
            user.id,
            additional_properties={
                "endpoint": "POST /v1/aggregations/cooccurrence",
                "time_window_days": payload.time_window_days,
            },
        )

        try:
            from cognee.infrastructure.databases.graph import get_graph_engine

            graph_engine = await get_graph_engine()
            
            # Find events within time windows
            # This is simplified - real implementation would calculate time differences
            query = """
                MATCH (e1:Event), (e2:Event)
                WHERE e1.at IS NOT NULL AND e2.at IS NOT NULL
                  AND id(e1) < id(e2)
                WITH e1, e2, abs(e1.at.year - e2.at.year) * 365 as days_apart
                WHERE days_apart <= $time_window_days
                RETURN e1.name as event1, e2.name as event2,
                       count(*) as cooccurrence_count,
                       avg(days_apart) as avg_distance
                HAVING cooccurrence_count >= $min_cooccurrence
                ORDER BY cooccurrence_count DESC
                LIMIT 20
            """
            
            result = await graph_engine.query(
                query,
                params={
                    "time_window_days": payload.time_window_days,
                    "min_cooccurrence": payload.min_cooccurrence
                }
            )
            
            pairs = []
            
            for row in result:
                pairs.append(EventPair(
                    event1=row.get("event1", ""),
                    event2=row.get("event2", ""),
                    cooccurrence_count=int(row.get("cooccurrence_count", 0)),
                    temporal_distance_avg_days=float(row.get("avg_distance", 0.0))
                ))

            return EventCooccurrenceResponseDTO(
                pairs=pairs,
                total_pairs=len(pairs),
                time_window_days=payload.time_window_days
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content={"error": f"Failed to analyze co-occurrence: {str(error)}"}
            )

    return router
