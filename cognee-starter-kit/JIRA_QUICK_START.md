# Jira Ticket Pipeline - Quick Start Guide

## 🚀 5-Minute Quick Start

### 1. Run the Simple Example
```bash
cd cognee-starter-kit
python src/pipelines/jira_simple_example.py
```

This will:
- Parse 3 example Jira tickets from XML
- Build a knowledge graph with ontology
- Run example queries
- Show ticket statistics

### 2. Check the Output
The example will display:
- ✅ Parsed tickets (PROJ-123, PROJ-124, PROJ-125)
- ✅ Knowledge graph creation status
- ✅ Query results (current status, priorities, etc.)
- ✅ Ticket statistics by status, priority, and type

### 3. View the Graph
Open the generated visualization:
```bash
# Location printed by the script
open src/pipelines/.artifacts/jira_graph_visualization.html
```

## 📊 What You'll See

### Example Tickets
1. **PROJ-123**: User authentication (In Progress, High priority)
2. **PROJ-124**: Database bug fix (Resolved, Critical priority)
3. **PROJ-125**: Dark mode feature (Open, Medium priority)

Each ticket includes:
- Full change history with timestamps
- User assignments
- Components and labels
- Status progression

### Example Queries
The simple example demonstrates:
- "What tickets are currently in progress?" → PROJ-123
- "Show me all critical priority tickets" → PROJ-124
- "What security-related tickets exist?" → PROJ-123 (has security label)
- "Tell me about PROJ-123" → Full ticket details

## 🎯 Next Steps

### Customize the Example
1. **Edit the data**: Modify `src/data/jira_tickets.xml`
2. **Add your tickets**: Follow the XML format
3. **Re-run**: `python src/pipelines/jira_simple_example.py`

### Try Advanced Features
```bash
# Full pipeline with versioning
python src/pipelines/jira_pipeline.py
```

This demonstrates:
- Both versioning strategies (UPDATE_LATEST and STORE_ALL_VERSIONS)
- Version retrieval functions
- More complex queries
- Temporal analysis

### Integrate with Real Jira

Replace XML parsing with Jira API:

```python
from jira import JIRA

# Connect to Jira
jira = JIRA('https://your-domain.atlassian.net', 
            basic_auth=('email', 'api_token'))

# Fetch tickets
issues = jira.search_issues('project=YOURPROJECT')

# Convert to XML or directly to JiraTicket objects
# Then use the pipeline as normal
```

## 📚 Documentation

- **[JIRA_PIPELINE_README.md](JIRA_PIPELINE_README.md)**: Complete usage guide
- **[VERSIONING_ANALYSIS.md](VERSIONING_ANALYSIS.md)**: Strategy comparison
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**: Technical details

## 🔑 Key Concepts

### Temporal Awareness
Tickets track time at multiple levels:
- Ticket timestamps: created, updated, resolved
- Change history: Every field change with timestamp
- Temporal queries: "What happened in February?"

### Ontology
The Jira ontology defines:
- Classes: Ticket, User, Status, Priority, etc.
- Relationships: assignedTo, hasStatus, hasComponent
- Properties: ticketId, summary, createdDate, etc.

This helps Cognee extract better entities and relationships.

### Versioning (Advanced)
Two strategies for handling updates:

**UPDATE_LATEST (Default)**
- Overwrites old version
- One node per ticket
- Fast and simple
- ✅ Recommended for most cases

**STORE_ALL_VERSIONS**
- Keeps all versions
- Multiple nodes per ticket
- Full history in graph
- Use only if required for compliance

## 🛠️ Common Tasks

### Query Current State
```python
import cognee
results = await cognee.search(
    query_text="What tickets are blocked?",
    query_type=SearchType.GRAPH_COMPLETION
)
```

### Analyze History
```python
from src.parsers.jira_xml_parser import parse_jira_xml

tickets = parse_jira_xml('src/data/jira_tickets.xml')
ticket = tickets[0]

# Get status changes
status_changes = ticket.get_changes_by_field("status")
print(f"Status progression: {[c.to_value for c in status_changes]}")

# Get changes in time range
recent = ticket.get_changes_in_timerange("2024-02-01", "2024-02-28")
print(f"February changes: {len(recent)}")
```

### Add Custom Fields
Edit `src/models/jira_models.py`:

```python
class JiraTicket(DataPoint):
    # ... existing fields ...
    
    # Add new fields
    story_points: Optional[int] = None
    sprint: Optional[str] = None
    epic_link: Optional[str] = None
```

## ⚡ Performance Tips

1. **Use UPDATE_LATEST**: Faster and simpler for most cases
2. **Batch ingestion**: Ingest multiple tickets at once
3. **Index optimization**: Add important fields to metadata['index_fields']
4. **Prune old data**: Regularly clean up unnecessary historical data

## 🐛 Troubleshooting

### "Module not found: cognee"
```bash
cd /path/to/cognee  # Main repo directory
pip install -e .
```

### "Ontology file not found"
Check that `src/data/jira_ontology.owl` exists, or run with `use_ontology=False`

### Queries return no results
- Verify tickets were ingested successfully
- Check that `cognify()` completed without errors
- Try simpler queries first

### Graph visualization is empty
- Ensure `index_graph_edges()` ran successfully
- Check that relationships are defined in ontology
- Verify tickets have proper structure

## 💡 Tips

1. **Start simple**: Use `jira_simple_example.py` first
2. **Understand your data**: Look at the XML structure
3. **Test queries**: Try different SearchType options
4. **Read the docs**: Check the detailed READMEs for advanced features
5. **Iterate**: Start with UPDATE_LATEST, add versioning only if needed

## 🎓 Learning Path

1. ✅ Run `jira_simple_example.py` (You are here!)
2. Read `JIRA_PIPELINE_README.md` for details
3. Try `jira_pipeline.py` for advanced features
4. Read `VERSIONING_ANALYSIS.md` to understand trade-offs
5. Customize models and ontology for your use case
6. Integrate with real Jira API

## 📞 Support

- Check documentation files in this directory
- Review example code in `src/pipelines/`
- Examine data models in `src/models/jira_models.py`
- Look at example data in `src/data/jira_tickets.xml`

## ✨ What's Next?

After mastering the basics:
- Add more ticket types and custom fields
- Integrate with Jira REST API
- Build custom dashboards
- Add automated syncing
- Implement SLA tracking
- Create predictive analytics

Happy ticket tracking! 🎫
