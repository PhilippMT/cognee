# Cognee - AI Memory Platform

Cognee is an open-source tool that transforms raw data into persistent, dynamic AI memory for agents. It combines vector search with graph databases to make documents both searchable by meaning and connected by relationships.

## Core Concept

Cognee replaces traditional RAG systems with ECL (Extract, Cognify, Load) pipelines that create a unified memory layer built on graphs and vectors.

## Key Operations

- `add()` - Ingest documents, text, or data into the system
- `cognify()` - Generate knowledge graphs from ingested data
- `memify()` - Add memory algorithms to the graph
- `search()` - Query the knowledge graph using combined relationships
- `update()` - Update existing data in the system
- `config()` - Configure system settings
- `datasets()` - Manage datasets
- `prune()` / `delete()` - Remove data from the system
- `visualize_graph()` - Visualize the knowledge graph
- `start_ui()` - Launch the web UI

## Search Types

- `GRAPH_COMPLETION` - Graph-based completion search
- `RAG_COMPLETION` - RAG-based completion search
- `CODE` - Code-specific search
- `CHUNKS` - Chunk-level search
- `SUMMARIES` - Summary search
- `CYPHER` - Direct Cypher query execution
- `FEELING_LUCKY` - Quick search mode

## Features

- Cloud sync capabilities with Cognee Cloud
- Thought graph generation and management
- Multi-user and multi-dataset support with access control
- Developer rules ingestion for AI coding assistants
- Code analysis and repository indexing
- MCP server for IDE and agent integration

## Use Cases

- Persistent agent memory for LLM applications
- GraphRAG implementations
- Document interconnection (conversations, files, images, audio)
- Knowledge graph generation and querying
- Code repository understanding and search
- Developer workflow integration via MCP
