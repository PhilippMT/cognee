# Jira Ticket Ingestion Pipeline

This pipeline demonstrates how to ingest Jira tickets into Cognee with full temporal awareness and ontology-based knowledge graph construction.

## Overview

The Jira pipeline provides:
- **XML parsing** of Jira ticket data with full history
- **Temporal awareness** tracking creation, updates, and changes over time
- **Ontology-based knowledge graph** defining ticket relationships
- **Two versioning strategies** for handling ticket updates
- **Graph-based search** for querying tickets and their relationships

## Files Structure

```
cognee-starter-kit/
├── src/
│   ├── data/
│   │   ├── jira_tickets.xml          # Example Jira ticket data
│   │   └── jira_ontology.owl         # Jira domain ontology
│   ├── models/
│   │   └── jira_models.py            # Jira ticket data models
│   ├── parsers/
│   │   └── jira_xml_parser.py        # XML parser for Jira tickets
│   └── pipelines/
│       └── jira_pipeline.py          # Main pipeline implementation
└── JIRA_PIPELINE_README.md           # This file
```

## Data Models

### JiraTicket
The main model with temporal awareness:
- `ticket_id`: Unique business identifier (e.g., "PROJ-123")
- `summary`, `description`: Ticket content
- `status`, `priority`, `ticket_type`: Current state
- `reporter`, `assignee`: User relationships
- `created_date`, `updated_date`, `resolved_date`: Temporal information
- `components`, `labels`: Categorization
- `history`: List of all changes with timestamps
- `version`: Version number for tracking updates

### Supporting Models
- **JiraUser**: Represents users in the system
- **JiraStatus**: Ticket status (Open, In Progress, Resolved, Closed)
- **JiraPriority**: Priority levels (Low, Medium, High, Critical)
- **JiraTicketType**: Ticket types (Story, Bug, Feature, Task)
- **JiraComponent**: Project components/modules
- **JiraLabel**: Tags for categorization
- **JiraHistoryChange**: Individual change record with timestamp

## Versioning Strategies

The pipeline supports two strategies for handling ticket updates:

### 1. UPDATE_LATEST (Default)
- Overwrites existing tickets with the same `ticket_id`
- Keeps only the most recent version
- Best for: Real-time dashboards, current state queries
- Storage efficient

```python
await execute_jira_pipeline(
    versioning=VersioningStrategy.UPDATE_LATEST
)
```

### 2. STORE_ALL_VERSIONS
- Stores all versions of each ticket
- Tracks version numbers automatically
- Retrieves latest version on query by default
- Best for: Audit trails, temporal analysis, change tracking
- More storage intensive

```python
await execute_jira_pipeline(
    versioning=VersioningStrategy.STORE_ALL_VERSIONS
)

# Retrieve specific versions
latest = get_latest_ticket_version("PROJ-123")
all_versions = get_all_ticket_versions("PROJ-123")
```

## Temporal Awareness

The pipeline tracks temporal information at multiple levels:

1. **Ticket-level timestamps**:
   - `created_date`: When ticket was created
   - `updated_date`: Last modification time
   - `resolved_date`: When ticket was resolved (if applicable)

2. **Change history**:
   - Each `JiraHistoryChange` has a `timestamp`
   - Tracks field-level changes (status, priority, assignee, etc.)
   - Records who made each change

3. **Temporal queries**:
   - Query tickets created/updated in date ranges
   - Track status progression over time
   - Analyze resolution times

## Ontology

The Jira ontology (`jira_ontology.owl`) defines:

### Classes
- Ticket, User, Status, Priority, TicketType, Component, Label, HistoryChange

### Object Properties (Relationships)
- `hasStatus`: Ticket → Status
- `hasPriority`: Ticket → Priority
- `hasType`: Ticket → TicketType
- `reportedBy`: Ticket → User
- `assignedTo`: Ticket → User
- `hasComponent`: Ticket → Component
- `hasLabel`: Ticket → Label
- `hasChange`: Ticket → HistoryChange

### Data Properties
- `ticketId`, `summary`, `description`
- `createdDate`, `updatedDate`, `resolvedDate`
- `changeTimestamp`, `fieldName`, `fromValue`, `toValue`

The ontology ensures that extracted entities and relationships follow the Jira domain model.

## Running the Pipeline

### Prerequisites
```bash
# From cognee-starter-kit directory
source .venv/bin/activate
```

### Run with default settings (UPDATE_LATEST strategy)
```bash
python src/pipelines/jira_pipeline.py
```

### Run programmatically with custom settings
```python
import asyncio
from src.pipelines.jira_pipeline import (
    execute_jira_pipeline,
    VersioningStrategy,
    get_latest_ticket_version,
    get_all_ticket_versions
)

async def run():
    # Run with STORE_ALL_VERSIONS strategy
    await execute_jira_pipeline(
        xml_path="path/to/your/jira_tickets.xml",
        use_ontology=True,
        versioning=VersioningStrategy.STORE_ALL_VERSIONS
    )
    
    # Query specific ticket
    latest = get_latest_ticket_version("PROJ-123")
    print(f"Latest status: {latest.status.name}")
    
    # Get full history
    all_versions = get_all_ticket_versions("PROJ-123")
    for version in all_versions:
        print(f"Version {version.version}: {version.status.name}")

asyncio.run(run())
```

## Example Queries

The pipeline includes example queries demonstrating various search capabilities:

1. **Status queries**: "What tickets are currently in progress?"
2. **Priority queries**: "Show me all critical priority tickets"
3. **Temporal queries**: "What tickets were created in February 2024?"
4. **History queries**: "Show me the history of PROJ-123"
5. **Label-based queries**: "What security-related tickets exist?"

## Example XML Format

The pipeline expects XML in the following format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jira-tickets>
    <ticket>
        <id>PROJ-123</id>
        <key>PROJ-123</key>
        <summary>Implement user authentication system</summary>
        <description>Need to implement a secure authentication system...</description>
        <status>In Progress</status>
        <priority>High</priority>
        <type>Story</type>
        <reporter>john.doe@example.com</reporter>
        <assignee>jane.smith@example.com</assignee>
        <created>2024-01-15T10:30:00Z</created>
        <updated>2024-02-20T14:45:00Z</updated>
        <resolved></resolved>
        <labels>
            <label>security</label>
            <label>authentication</label>
        </labels>
        <components>
            <component>API</component>
            <component>Security</component>
        </components>
        <history>
            <change>
                <timestamp>2024-01-15T10:30:00Z</timestamp>
                <field>status</field>
                <from></from>
                <to>Open</to>
                <author>john.doe@example.com</author>
            </change>
            <!-- More changes... -->
        </history>
    </ticket>
    <!-- More tickets... -->
</jira-tickets>
```

## Best Practices for Ingesting Updates

### For Real-time Systems (UPDATE_LATEST)
1. **Periodic polling**: Poll Jira API at intervals (e.g., every 15 minutes)
2. **Incremental updates**: Only fetch tickets modified since last poll
3. **Pipeline runs**: Re-run pipeline with new XML data
4. **Result**: Graph always reflects current state

```python
# Pseudo-code for periodic updates
while True:
    # Fetch tickets modified since last_update_time
    new_tickets = fetch_jira_updates(since=last_update_time)
    
    # Write to XML
    write_jira_xml(new_tickets, "jira_updates.xml")
    
    # Run pipeline (overwrites old versions)
    await execute_jira_pipeline(
        xml_path="jira_updates.xml",
        versioning=VersioningStrategy.UPDATE_LATEST
    )
    
    last_update_time = now()
    await asyncio.sleep(900)  # 15 minutes
```

### For Audit/History Systems (STORE_ALL_VERSIONS)
1. **Version detection**: Compare ticket `updated_date` to detect changes
2. **Append-only**: New versions are added, old versions preserved
3. **Query latest**: Use `get_latest_ticket_version()` for current state
4. **Temporal analysis**: Use `get_all_ticket_versions()` for history

```python
# Pseudo-code for version tracking
new_tickets = fetch_jira_updates()

# Pipeline automatically detects and versions changes
await execute_jira_pipeline(
    xml_path="jira_updates.xml",
    versioning=VersioningStrategy.STORE_ALL_VERSIONS
)

# Analyze changes over time
for ticket_id in changed_tickets:
    versions = get_all_ticket_versions(ticket_id)
    analyze_status_progression(versions)
    calculate_time_to_resolution(versions)
```

## Recommendation

Based on analysis, we recommend:

**UPDATE_LATEST for most use cases** because:
- Simpler to reason about (one current state per ticket)
- More storage efficient
- Faster queries
- Sufficient for 90% of Jira analytics needs

**STORE_ALL_VERSIONS for specialized cases**:
- Compliance/audit requirements
- Process improvement analysis (cycle time trends)
- Root cause analysis of delays
- Historical what-if scenarios

You can always store change history in `JiraHistoryChange` objects even with UPDATE_LATEST strategy, which gives you detailed temporal information without full version storage.

## Visualization

After running the pipeline, open the generated graph visualization:
```bash
open src/pipelines/.artifacts/jira_graph_visualization.html
```

The graph shows:
- Ticket nodes with status indicators
- User nodes and assignment relationships
- Component and label groupings
- Temporal edges for change history
- Priority and type classifications

## Extending the Pipeline

### Add Custom Fields
Modify `jira_models.py` to add fields:
```python
class JiraTicket(DataPoint):
    # ... existing fields ...
    story_points: Optional[int] = None
    sprint: Optional[str] = None
```

### Add Custom Queries
Add to `run_example_queries()`:
```python
{
    "text": "What tickets are overdue?",
    "type": SearchType.GRAPH_COMPLETION
}
```

### Integrate Jira API
Replace XML parsing with API calls:
```python
from jira import JIRA

def fetch_jira_tickets():
    jira = JIRA('https://your-domain.atlassian.net', 
                basic_auth=('email', 'api_token'))
    issues = jira.search_issues('project=PROJ')
    # Convert to JiraTicket objects
    return [convert_issue_to_ticket(issue) for issue in issues]
```

## Troubleshooting

### Pipeline fails with "ontology file not found"
- Ensure `jira_ontology.owl` exists in `src/data/`
- Or run with `use_ontology=False`

### Graph visualization doesn't show relationships
- Check that `index_graph_edges()` completed successfully
- Verify ontology defines expected relationships

### Temporal queries return no results
- Ensure tickets have valid ISO 8601 timestamps
- Check date range matches data in XML

## Next Steps

1. **Connect to real Jira instance** using Jira REST API
2. **Add automated syncing** with scheduled pipeline runs
3. **Create custom dashboards** using graph queries
4. **Implement alerting** for ticket SLA breaches
5. **Add ML predictions** for resolution times based on history
