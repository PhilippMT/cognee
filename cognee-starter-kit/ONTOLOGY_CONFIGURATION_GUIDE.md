# Ontology Configuration Guide

This guide explains how to configure ontologies in Cognee, including automatic application using environment variables.

## Overview

Cognee supports ontology-based knowledge graph construction to improve entity extraction and relationship modeling. Ontologies can be configured in two ways:

1. **Programmatically** - Pass ontology configuration directly in code
2. **Environment Variables** - Configure via `.env` file for automatic application

## Configuration Methods

### Method 1: Programmatic Configuration (Recommended for Flexibility)

This method gives you full control and is demonstrated in the examples:

```python
import cognee
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver
from cognee.modules.ontology.ontology_config import Config

# Specify ontology file path
ontology_path = "/path/to/your/ontology.owl"

# Create configuration
config: Config = {
    "ontology_config": {
        "ontology_resolver": RDFLibOntologyResolver(ontology_file=ontology_path)
    }
}

# Run cognify with ontology
await cognee.cognify(config=config)
```

**Advantages:**
- ✅ Explicit and clear which ontology is used
- ✅ Easy to switch between ontologies for different pipelines
- ✅ Can use different ontologies in the same application
- ✅ No global state concerns

### Method 2: Environment Variable Configuration (Automatic Application)

Configure ontology globally via environment variables for automatic application.

#### Step 1: Configure `.env` File

Add the following to your `.env` file:

```bash
# -- Ontology resolver params --------------------------------------
ONTOLOGY_RESOLVER=rdflib  # Default: uses rdflib and owl file to read ontology structures
MATCHING_STRATEGY=fuzzy   # Default: uses fuzzy matching with 80% similarity threshold
ONTOLOGY_FILE_PATH=/absolute/path/to/your/ontology.owl  # MUST be absolute path
```

#### Step 2: Use in Code

When environment variables are set, Cognee will automatically load and apply the ontology:

```python
import cognee

# No need to pass ontology config - it's loaded from env
await cognee.cognify()
```

**Important Notes:**
- ⚠️ `ONTOLOGY_FILE_PATH` **must be an absolute path**
- ⚠️ The ontology is applied globally to all `cognify()` calls
- ⚠️ To disable, remove or comment out the environment variables

## Environment Variable Reference

### ONTOLOGY_RESOLVER

Specifies which ontology resolver implementation to use.

**Values:**
- `rdflib` (default) - Uses RDFLib library to parse OWL/RDF files

**Example:**
```bash
ONTOLOGY_RESOLVER=rdflib
```

### MATCHING_STRATEGY

Defines how extracted entities are matched against ontology classes.

**Values:**
- `fuzzy` (default) - Uses fuzzy string matching with 80% similarity threshold
- `exact` - Requires exact string matches (case-insensitive)

**Example:**
```bash
MATCHING_STRATEGY=fuzzy
```

**How it works:**
- **Fuzzy matching**: "InProgress" matches "In Progress" (80%+ similar)
- **Exact matching**: Only exact strings match (after case normalization)

### ONTOLOGY_FILE_PATH

Path to your ontology file (OWL format).

**Requirements:**
- ✅ Must be an absolute path
- ✅ File must exist and be readable
- ✅ Must be valid OWL/RDF XML format

**Example:**
```bash
ONTOLOGY_FILE_PATH=/home/user/project/cognee-starter-kit/src/data/jira_ontology.owl
```

**Common mistake:**
```bash
# ❌ WRONG - relative path
ONTOLOGY_FILE_PATH=./src/data/jira_ontology.owl

# ✅ CORRECT - absolute path
ONTOLOGY_FILE_PATH=/home/user/project/src/data/jira_ontology.owl
```

## Available Ontologies

### 1. jira_ontology.owl (Original Format)

Ontology for custom Jira XML format with history tracking.

**Use case:** Custom Jira exports with change history

**Location:** `cognee-starter-kit/src/data/jira_ontology.owl`

**Classes:**
- Ticket, User, Status, Priority, TicketType
- Component, Label, HistoryChange

**Configuration:**
```bash
ONTOLOGY_FILE_PATH=/path/to/cognee-starter-kit/src/data/jira_ontology.owl
```

### 2. jira_rss_ontology.owl (NEW - RSS Format)

Ontology for Jira RSS feed format (standard Jira XML export).

**Use case:** Standard Jira RSS exports with comments and parent issues

**Location:** `cognee-starter-kit/src/data/jira_rss_ontology.owl`

**Classes:**
- Issue, User, Project, Status, StatusCategory
- Priority, IssueType, Component, Label
- Resolution, Comment, ParentIssue

**Key differences from original:**
- RSS feed structure (`<item>` elements in `<channel>`)
- Includes comments as separate entities
- Has parent issue relationships (Epic → Story)
- Includes status categories and resolutions
- Project information included

**Configuration:**
```bash
ONTOLOGY_FILE_PATH=/path/to/cognee-starter-kit/src/data/jira_rss_ontology.owl
```

## Complete Configuration Examples

### Example 1: Jira Pipeline with Original Format

**`.env` configuration:**
```bash
# Ontology for custom Jira XML format
ONTOLOGY_RESOLVER=rdflib
MATCHING_STRATEGY=fuzzy
ONTOLOGY_FILE_PATH=/home/user/cognee-starter-kit/src/data/jira_ontology.owl
```

**Code:**
```python
# Automatic ontology loading from env
await cognee.cognify()
```

### Example 2: Jira Pipeline with RSS Format

**`.env` configuration:**
```bash
# Ontology for Jira RSS format
ONTOLOGY_RESOLVER=rdflib
MATCHING_STRATEGY=fuzzy
ONTOLOGY_FILE_PATH=/home/user/cognee-starter-kit/src/data/jira_rss_ontology.owl
```

**Code:**
```python
# Automatic ontology loading from env
await cognee.cognify()
```

### Example 3: Override Environment Variables

If environment variables are set but you want to use a different ontology:

```python
# Programmatic config overrides environment variables
ontology_path = "/path/to/different_ontology.owl"
config: Config = {
    "ontology_config": {
        "ontology_resolver": RDFLibOntologyResolver(ontology_file=ontology_path)
    }
}

await cognee.cognify(config=config)
```

### Example 4: Disable Ontology Temporarily

To disable ontology when environment variables are set:

```python
# Pass empty config to disable ontology
config: Config = {
    "ontology_config": None
}

await cognee.cognify(config=config)
```

## How Ontology Application Works

### 1. Configuration Priority

The configuration is applied in this order (highest to lowest priority):

1. **Programmatic config** - Passed to `cognify(config=...)`
2. **Environment variables** - From `.env` file
3. **Default** - No ontology (if neither is provided)

### 2. Ontology Loading Process

When ontology is configured, Cognee:

1. **Loads the ontology file** using the specified resolver
2. **Parses classes and relationships** from OWL/RDF structure
3. **Extracts entities** from your data (text, documents, tickets)
4. **Matches entities** to ontology classes using the matching strategy
5. **Creates graph nodes** with proper types from ontology
6. **Establishes relationships** based on ontology properties

### 3. Benefits of Using Ontology

**Without ontology:**
```
Text: "PROJ-123 is a high priority story assigned to John"

Graph:
  Node: "PROJ-123" (generic entity)
  Node: "high priority" (generic entity)
  Node: "story" (generic entity)
  Node: "John" (generic entity)
```

**With ontology:**
```
Text: "PROJ-123 is a high priority story assigned to John"

Graph:
  Node: "PROJ-123" (type: Issue)
  Node: "High" (type: Priority)
  Node: "Story" (type: IssueType)
  Node: "John" (type: User)
  
Relationships:
  PROJ-123 --hasPriority--> High
  PROJ-123 --hasType--> Story
  PROJ-123 --assignedTo--> John
```

## Troubleshooting

### Issue: Ontology not loading

**Symptoms:**
- No error but ontology doesn't seem to apply
- Entities extracted without proper types

**Solutions:**
1. Check `ONTOLOGY_FILE_PATH` is absolute path
2. Verify file exists: `ls -la $ONTOLOGY_FILE_PATH`
3. Ensure file is valid OWL/RDF XML
4. Check file permissions (readable)

### Issue: Path not found error

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: './src/data/jira_ontology.owl'
```

**Solution:**
Use absolute path, not relative:
```bash
# Get absolute path
cd cognee-starter-kit
pwd  # e.g., /home/user/cognee-starter-kit

# Set in .env
ONTOLOGY_FILE_PATH=/home/user/cognee-starter-kit/src/data/jira_ontology.owl
```

### Issue: Wrong ontology applied

**Symptoms:**
- Using RSS format data but entities match original format
- Or vice versa

**Solution:**
1. Check which ontology is configured in `.env`
2. Ensure `ONTOLOGY_FILE_PATH` points to correct file:
   - `jira_ontology.owl` - Original format
   - `jira_rss_ontology.owl` - RSS format
3. Match ontology to your data format

### Issue: Fuzzy matching too lenient

**Symptoms:**
- Incorrect entities matched (e.g., "Status" matching "Static")

**Solution:**
Change to exact matching:
```bash
MATCHING_STRATEGY=exact
```

## Best Practices

### 1. Choose Configuration Method Based on Use Case

**Use programmatic configuration when:**
- Building reusable libraries
- Need different ontologies per pipeline
- Want explicit control in code
- Testing different ontologies

**Use environment variables when:**
- Single ontology for entire application
- Deploying to production with consistent config
- Want simplified code (no config passing)
- Team prefers configuration files

### 2. Version Control

**✅ DO:**
- Commit `.env.template` with example values
- Commit ontology files (`.owl`)
- Document which ontology to use for which data format

**❌ DON'T:**
- Commit actual `.env` file (add to `.gitignore`)
- Use relative paths in committed examples

### 3. Documentation

In your README or pipeline documentation, specify:
- Which ontology file to use
- What `.env` settings are needed
- Example absolute path (with placeholder username)

Example:
```markdown
## Setup

1. Copy `.env.template` to `.env`
2. Set ontology path:
   ```
   ONTOLOGY_FILE_PATH=/home/YOUR_USERNAME/cognee-starter-kit/src/data/jira_rss_ontology.owl
   ```
3. Run pipeline
```

### 4. Testing

Test both with and without ontology:

```python
# Test 1: Without ontology
await cognee.cognify()

# Test 2: With ontology (env)
# (Set ONTOLOGY_FILE_PATH in .env first)
await cognee.cognify()

# Test 3: With specific ontology (programmatic)
config = {"ontology_config": {"ontology_resolver": RDFLibOntologyResolver(ontology_file=path)}}
await cognee.cognify(config=config)
```

## Summary

| Feature | Programmatic | Environment Variables |
|---------|-------------|----------------------|
| Configuration | In code | In `.env` file |
| Flexibility | High | Medium |
| Ease of use | Medium | High (once configured) |
| Global state | No | Yes |
| Multi-ontology | Easy | Need to change `.env` |
| Recommended for | Libraries, testing | Production, single ontology |

**Recommendation:** Start with programmatic configuration for learning and testing. Move to environment variables for production if you use a single ontology consistently.

## Additional Resources

- **Examples:**
  - `examples/python/ontology_demo_example.py` - Basic ontology usage
  - `examples/python/ontology_demo_example_2.py` - Medical ontology example
  - `cognee-starter-kit/src/pipelines/jira_pipeline.py` - Jira with ontology

- **Ontology Files:**
  - `src/data/jira_ontology.owl` - Original Jira format
  - `src/data/jira_rss_ontology.owl` - RSS format (NEW)

- **Documentation:**
  - `JIRA_PIPELINE_README.md` - Jira pipeline guide
  - `VERSIONING_ANALYSIS.md` - Strategy analysis
