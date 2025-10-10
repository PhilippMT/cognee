"""Jira ticket models with temporal awareness."""

from typing import List, Optional
from datetime import datetime
from cognee.low_level import DataPoint


class JiraUser(DataPoint):
    """Represents a Jira user."""
    
    email: str
    name: Optional[str] = None
    metadata: dict = {"index_fields": ["email", "name"]}


class JiraStatus(DataPoint):
    """Represents a ticket status."""
    
    name: str
    metadata: dict = {"index_fields": ["name"]}


class JiraPriority(DataPoint):
    """Represents a ticket priority."""
    
    name: str
    metadata: dict = {"index_fields": ["name"]}


class JiraTicketType(DataPoint):
    """Represents a ticket type (Story, Bug, Feature, Task)."""
    
    name: str
    metadata: dict = {"index_fields": ["name"]}


class JiraComponent(DataPoint):
    """Represents a project component."""
    
    name: str
    metadata: dict = {"index_fields": ["name"]}


class JiraLabel(DataPoint):
    """Represents a label for categorization."""
    
    name: str
    metadata: dict = {"index_fields": ["name"]}


class JiraHistoryChange(DataPoint):
    """Represents a change in ticket history with temporal information."""
    
    timestamp: str  # ISO 8601 format
    field: str
    from_value: str
    to_value: str
    author: JiraUser
    metadata: dict = {"index_fields": ["field", "timestamp"]}


class JiraTicket(DataPoint):
    """
    Represents a Jira ticket with full temporal awareness.
    
    This model tracks:
    - Creation, update, and resolution timestamps
    - Current status, priority, type
    - Relationships to users, components, labels
    - Full history of changes with timestamps
    
    Versioning strategy:
    - ticket_id is the unique business identifier
    - DataPoint.id is the internal UUID
    - version tracks updates to the same ticket_id
    - created_at and updated_at track temporal changes
    """
    
    ticket_id: str  # Jira ticket ID (e.g., PROJ-123)
    key: str  # Same as ticket_id for compatibility
    summary: str
    description: str
    
    # Current state
    status: JiraStatus
    priority: JiraPriority
    ticket_type: JiraTicketType
    
    # Users
    reporter: JiraUser
    assignee: Optional[JiraUser] = None
    
    # Timestamps (ISO 8601 format strings for easy querying)
    created_date: str
    updated_date: str
    resolved_date: Optional[str] = None
    
    # Relationships
    components: List[JiraComponent] = []
    labels: List[JiraLabel] = []
    history: List[JiraHistoryChange] = []
    
    # Metadata for indexing and search
    metadata: dict = {"index_fields": ["ticket_id", "summary", "description", "status"]}
    
    def get_latest_change(self) -> Optional[JiraHistoryChange]:
        """Get the most recent history change."""
        if not self.history:
            return None
        return max(self.history, key=lambda x: x.timestamp)
    
    def get_changes_by_field(self, field_name: str) -> List[JiraHistoryChange]:
        """Get all changes for a specific field."""
        return [change for change in self.history if change.field == field_name]
    
    def get_changes_in_timerange(self, start: str, end: str) -> List[JiraHistoryChange]:
        """Get changes within a time range."""
        return [
            change for change in self.history 
            if start <= change.timestamp <= end
        ]
