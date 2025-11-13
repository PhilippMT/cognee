"""
Coding Agent Chat Session - Data Models

This module defines the data models for representing coding agent chat sessions,
messages, extracted facts, and development status in a temporal-aware graph.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from cognee.infrastructure.engine import DataPoint


class ChatMessage(DataPoint):
    """Represents a single message in a coding agent chat session."""
    
    session_id: str = Field(..., description="Unique identifier for the chat session")
    message_id: str = Field(..., description="Unique identifier for this message")
    role: str = Field(..., description="Role: user, assistant, agent, tool, system")
    content: str = Field(..., description="Message content/text")
    timestamp: datetime = Field(..., description="When the message was sent")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Tool calls made in this message"
    )
    parent_message_id: Optional[str] = Field(None, description="ID of parent message if reply")
    
    metadata: dict = {"index_fields": ["session_id", "role", "content"]}


class DevelopmentFact(DataPoint):
    """Represents an extracted fact about development activities."""
    
    fact_type: str = Field(
        ...,
        description="Type: code_change, bug_fix, feature, refactor, decision, dependency"
    )
    description: str = Field(..., description="Description of the fact")
    status: str = Field(
        ...,
        description="Status: planned, in_progress, completed, blocked, cancelled"
    )
    valid_at: datetime = Field(..., description="When this fact became true")
    invalid_at: Optional[datetime] = Field(None, description="When this fact became invalid")
    session_id: str = Field(..., description="Associated session ID")
    related_message_ids: List[str] = Field(
        default=[],
        description="Messages that contributed to this fact"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for this fact"
    )
    entities: List[str] = Field(
        default=[],
        description="Related code entities (files, functions, classes)"
    )
    
    metadata: dict = {"index_fields": ["fact_type", "status", "description"]}


class AgentDecision(DataPoint):
    """Represents a decision made by the agent during development."""
    
    decision: str = Field(..., description="The decision that was made")
    rationale: str = Field(..., description="Reasoning behind the decision")
    alternatives: List[str] = Field(default=[], description="Alternative options considered")
    outcome: Optional[str] = Field(None, description="Result of implementing this decision")
    timestamp: datetime = Field(..., description="When the decision was made")
    session_id: str = Field(..., description="Associated session ID")
    message_id: str = Field(..., description="Message where decision was made")
    decision_type: str = Field(
        ...,
        description="Type: technical, architectural, tooling, approach"
    )
    impact: str = Field(
        default="medium",
        description="Impact level: low, medium, high, critical"
    )
    
    metadata: dict = {"index_fields": ["decision", "rationale", "decision_type"]}


class CodeEntity(DataPoint):
    """Represents a code entity discussed in the session."""
    
    entity_type: str = Field(
        ...,
        description="Type: file, function, class, module, variable, constant"
    )
    entity_name: str = Field(..., description="Name of the code entity")
    description: Optional[str] = Field(None, description="Description of the entity")
    file_path: Optional[str] = Field(None, description="File path if applicable")
    language: Optional[str] = Field(None, description="Programming language")
    first_mentioned: datetime = Field(..., description="When first mentioned")
    last_mentioned: datetime = Field(..., description="When last mentioned")
    session_id: str = Field(..., description="Associated session ID")
    modifications: List[Dict[str, Any]] = Field(
        default=[],
        description="List of modifications made to this entity"
    )
    
    metadata: dict = {"index_fields": ["entity_name", "entity_type", "description"]}


class SessionMetadata(DataPoint):
    """Metadata and summary information for a chat session."""
    
    session_id: str = Field(..., description="Unique session identifier")
    session_goal: Optional[str] = Field(None, description="Primary goal of the session")
    session_type: str = Field(
        ...,
        description="Type: debugging, feature_development, refactoring, exploration, review"
    )
    start_time: datetime = Field(..., description="Session start time")
    end_time: Optional[datetime] = Field(None, description="Session end time")
    participants: List[Dict[str, str]] = Field(
        default=[],
        description="List of participants with roles"
    )
    outcome: Optional[str] = Field(None, description="Session outcome/result")
    completion_status: str = Field(
        default="in_progress",
        description="Status: in_progress, completed, abandoned"
    )
    message_count: int = Field(default=0, description="Total number of messages")
    tool_calls_count: int = Field(default=0, description="Total number of tool calls")
    code_changes: List[str] = Field(default=[], description="List of files changed")
    related_sessions: List[str] = Field(
        default=[],
        description="IDs of related sessions"
    )
    tags: List[str] = Field(default=[], description="Session tags")
    
    metadata: dict = {"index_fields": ["session_goal", "session_type", "outcome"]}


class InteractionPattern(DataPoint):
    """Represents a recurring interaction pattern in chat sessions."""
    
    pattern_type: str = Field(
        ...,
        description="Type: question_answer, error_resolution, clarification, confirmation"
    )
    description: str = Field(..., description="Description of the pattern")
    trigger: str = Field(..., description="What triggers this pattern")
    response: str = Field(..., description="Typical response in this pattern")
    frequency: int = Field(default=1, description="How many times observed")
    sessions: List[str] = Field(
        default=[],
        description="Sessions where this pattern occurred"
    )
    effectiveness: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="How effective this pattern is"
    )
    
    metadata: dict = {"index_fields": ["pattern_type", "description", "trigger"]}


class DevelopmentTimeline(DataPoint):
    """Represents a timeline of development activities in a session."""
    
    session_id: str = Field(..., description="Associated session ID")
    events: List[Dict[str, Any]] = Field(
        default=[],
        description="Chronological list of development events"
    )
    milestones: List[Dict[str, Any]] = Field(
        default=[],
        description="Key milestones achieved"
    )
    blockers: List[Dict[str, Any]] = Field(
        default=[],
        description="Blockers encountered and their resolution"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    
    metadata: dict = {"index_fields": ["session_id"]}
