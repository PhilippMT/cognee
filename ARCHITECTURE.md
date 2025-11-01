# Cognee Architecture Documentation

> **Comprehensive architectural visualizations for Cognee - Memory Layer for AI Agents**

This document provides detailed architectural diagrams explaining the Cognee system from high-level concepts down to low-level implementation details. Each diagram focuses on a specific aspect of the architecture to provide clarity and understanding.

## Table of Contents

1. [High-Level Architecture Overview](#1-high-level-architecture-overview)
2. [Core Workflow - ECL Pipeline](#2-core-workflow---ecl-pipeline)
3. [System Components Architecture](#3-system-components-architecture)
4. [Infrastructure Layer](#4-infrastructure-layer)
5. [Database Architecture](#5-database-architecture)
6. [API Layer Architecture](#6-api-layer-architecture)
7. [Pipeline Processing System](#7-pipeline-processing-system)
8. [Module Dependencies](#8-module-dependencies)
9. [Data Flow - Add Operation](#9-data-flow---add-operation)
10. [Data Flow - Cognify Operation](#10-data-flow---cognify-operation)
11. [Data Flow - Memify Operation](#11-data-flow---memify-operation)
12. [Data Flow - Search Operation](#12-data-flow---search-operation)
13. [LLM Integration Architecture](#13-llm-integration-architecture)
14. [Vector Database Integration](#14-vector-database-integration)
15. [Graph Database Integration](#15-graph-database-integration)
16. [Task System Architecture](#16-task-system-architecture)
17. [Chunking Strategy](#17-chunking-strategy)
18. [Retrieval System](#18-retrieval-system)
19. [Knowledge Graph Construction](#19-knowledge-graph-construction)
20. [Authentication & Permissions](#20-authentication--permissions)
21. [Configuration Management](#21-configuration-management)
22. [Observability & Monitoring](#22-observability--monitoring)
23. [Deployment Architecture](#23-deployment-architecture)

---

## 1. High-Level Architecture Overview

The highest-level view of Cognee showing the main conceptual components and their relationships.

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[CLI Interface]
        API[REST API]
        SDK[Python SDK]
    end
    
    subgraph "Core Processing Layer"
        ADD[Add/Ingest]
        COGNIFY[Cognify/Process]
        MEMIFY[Memify/Enrich]
        SEARCH[Search/Query]
    end
    
    subgraph "Infrastructure Layer"
        LLM[LLM Gateway<br/>OpenAI, Anthropic, etc.]
        VECTOR[Vector DB<br/>LanceDB, Qdrant, etc.]
        GRAPH[Graph DB<br/>Kuzu, Neo4j, etc.]
        RELATIONAL[Relational DB<br/>SQLite, PostgreSQL]
        STORAGE[File Storage<br/>Local, S3]
    end
    
    CLI --> ADD
    API --> ADD
    SDK --> ADD
    
    ADD --> COGNIFY
    COGNIFY --> MEMIFY
    MEMIFY --> SEARCH
    
    ADD --> STORAGE
    COGNIFY --> LLM
    COGNIFY --> VECTOR
    COGNIFY --> GRAPH
    MEMIFY --> GRAPH
    SEARCH --> VECTOR
    SEARCH --> GRAPH
    SEARCH --> LLM
    
    ADD --> RELATIONAL
    COGNIFY --> RELATIONAL
    MEMIFY --> RELATIONAL
    SEARCH --> RELATIONAL
    
    style ADD fill:#a8e6cf
    style COGNIFY fill:#ffd3b6
    style MEMIFY fill:#ffaaa5
    style SEARCH fill:#ff8b94
```

**Description:** This diagram shows how Cognee transforms unstructured data into an intelligent knowledge graph through the ECL (Extract, Cognify, Load) pipeline. Users interact through CLI, REST API, or Python SDK to add data, process it into knowledge graphs, enrich with memory algorithms, and search for insights.

---

## 2. Core Workflow - ECL Pipeline

The Extract-Cognify-Load workflow that forms the heart of Cognee's processing.

```mermaid
sequenceDiagram
    participant User
    participant Cognee
    participant Storage
    participant LLM
    participant VectorDB
    participant GraphDB
    
    Note over User,GraphDB: ADD Phase - Data Ingestion
    User->>Cognee: cognee.add(data)
    Cognee->>Storage: Store raw data
    Cognee->>Cognee: Extract text/content
    Cognee->>Storage: Store extracted content
    Cognee-->>User: Data added
    
    Note over User,GraphDB: COGNIFY Phase - Knowledge Graph Creation
    User->>Cognee: cognee.cognify()
    Cognee->>Cognee: Classify documents
    Cognee->>Cognee: Chunk text
    Cognee->>LLM: Extract entities & relationships
    LLM-->>Cognee: Entity/relationship data
    Cognee->>VectorDB: Store embeddings
    Cognee->>GraphDB: Build knowledge graph
    Cognee->>LLM: Generate summaries
    Cognee-->>User: Knowledge graph created
    
    Note over User,GraphDB: MEMIFY Phase - Graph Enrichment
    User->>Cognee: cognee.memify()
    Cognee->>GraphDB: Extract subgraph
    Cognee->>LLM: Apply memory algorithms
    LLM-->>Cognee: Enriched relationships
    Cognee->>GraphDB: Update graph with enrichments
    Cognee-->>User: Graph enriched
    
    Note over User,GraphDB: SEARCH Phase - Query & Retrieve
    User->>Cognee: cognee.search(query)
    Cognee->>VectorDB: Semantic search
    VectorDB-->>Cognee: Relevant chunks
    Cognee->>GraphDB: Graph traversal
    GraphDB-->>Cognee: Related entities
    Cognee->>LLM: Generate completion
    LLM-->>Cognee: Final answer
    Cognee-->>User: Search results
```

**Description:** This sequence diagram illustrates the complete lifecycle of data through Cognee, from ingestion to intelligent query responses, showing how each phase interacts with different infrastructure components.

---

## 3. System Components Architecture

Detailed breakdown of all major system components and their relationships.

```mermaid
graph TB
    subgraph "cognee Package"
        subgraph "API Layer (api/)"
            V1[v1 API Endpoints]
            ADD_API[add.py]
            COGNIFY_API[cognify.py]
            SEARCH_API[search.py]
            DATASETS_API[datasets.py]
            PRUNE_API[prune.py]
            CONFIG_API[config.py]
        end
        
        subgraph "Infrastructure (infrastructure/)"
            LLM_INFRA[LLM Integration]
            DB_INFRA[Database Adapters]
            FILE_INFRA[File Management]
            LOADER_INFRA[Data Loaders]
            ENGINE_INFRA[Engine Models]
        end
        
        subgraph "Modules (modules/)"
            PIPELINES[Pipelines System]
            CHUNKING[Chunking]
            SEARCH_MOD[Search/Retrieval]
            MEMIFY_MOD[Memify]
            COGNIFY_MOD[Cognify]
            USERS[User Management]
            DATA[Data Management]
            ONTOLOGY[Ontology]
            VISUALIZATION[Visualization]
        end
        
        subgraph "Tasks (tasks/)"
            DOC_TASKS[Document Tasks]
            GRAPH_TASKS[Graph Tasks]
            STORAGE_TASKS[Storage Tasks]
            SUMM_TASKS[Summarization Tasks]
            ENTITY_TASKS[Entity Tasks]
            TEMPORAL_TASKS[Temporal Tasks]
        end
        
        subgraph "Shared (shared/)"
            LOGGING[Logging Utils]
            DATA_MODELS[Data Models]
        end
    end
    
    V1 --> ADD_API
    V1 --> COGNIFY_API
    V1 --> SEARCH_API
    V1 --> DATASETS_API
    
    ADD_API --> PIPELINES
    COGNIFY_API --> PIPELINES
    SEARCH_API --> SEARCH_MOD
    
    PIPELINES --> DOC_TASKS
    PIPELINES --> GRAPH_TASKS
    PIPELINES --> STORAGE_TASKS
    
    COGNIFY_MOD --> CHUNKING
    COGNIFY_MOD --> ONTOLOGY
    
    SEARCH_MOD --> DB_INFRA
    SEARCH_MOD --> LLM_INFRA
    
    DOC_TASKS --> FILE_INFRA
    GRAPH_TASKS --> DB_INFRA
    STORAGE_TASKS --> DB_INFRA
    
    DB_INFRA --> ENGINE_INFRA
    
    PIPELINES --> LOGGING
    SEARCH_MOD --> DATA_MODELS
    
    style V1 fill:#e1f5ff
    style PIPELINES fill:#fff9e1
    style DB_INFRA fill:#ffe1f5
```

**Description:** This diagram shows the modular architecture of Cognee, with clear separation between API endpoints, core modules, infrastructure services, task implementations, and shared utilities.

---

## 4. Infrastructure Layer

Deep dive into the infrastructure components that power Cognee.

```mermaid
graph LR
    subgraph "Infrastructure Layer"
        subgraph "LLM (llm/)"
            GATEWAY[LLMGateway]
            TOKENIZER[Tokenizer]
            PROMPTS[Prompt Templates]
            STRUCTURED[Structured Output]
            EXTRACTION[Content Extraction]
        end
        
        subgraph "Databases (databases/)"
            VECTOR_INT[Vector Interface]
            GRAPH_INT[Graph Interface]
            REL_INT[Relational Interface]
            CACHE_INT[Cache Interface]
            HYBRID_INT[Hybrid Interface]
        end
        
        subgraph "Files (files/)"
            STORAGE_MGR[Storage Manager]
            FILE_UTILS[File Utilities]
        end
        
        subgraph "Loaders (loaders/)"
            CORE_LOADERS[Core Loaders]
            EXTERNAL_LOADERS[External Loaders]
            LOADER_UTILS[Loader Utils]
        end
        
        subgraph "Context"
            CTX_MGR[Context Manager]
        end
        
        subgraph "Engine (engine/)"
            ENG_MODELS[Engine Models]
            ENG_UTILS[Engine Utils]
        end
        
        subgraph "Data (data/)"
            CHUNKING_DATA[Chunking Logic]
            DATA_UTILS[Data Utils]
        end
    end
    
    GATEWAY --> TOKENIZER
    GATEWAY --> PROMPTS
    GATEWAY --> STRUCTURED
    
    VECTOR_INT --> ENG_MODELS
    GRAPH_INT --> ENG_MODELS
    REL_INT --> ENG_MODELS
    
    STORAGE_MGR --> FILE_UTILS
    CORE_LOADERS --> LOADER_UTILS
    EXTERNAL_LOADERS --> LOADER_UTILS
    
    CHUNKING_DATA --> DATA_UTILS
    
    style GATEWAY fill:#a8e6cf
    style VECTOR_INT fill:#ffd3b6
    style GRAPH_INT fill:#ffaaa5
    style STORAGE_MGR fill:#ff8b94
```

**Description:** The infrastructure layer provides abstracted interfaces to external services like LLMs, databases, and storage systems, allowing Cognee to be provider-agnostic and easily configurable.

---

## 5. Database Architecture

Multi-database architecture supporting vector, graph, and relational storage.

```mermaid
graph TB
    subgraph "Database Layer"
        subgraph "Vector Databases"
            LANCE[LanceDB<br/>Default]
            QDRANT[Qdrant]
            WEAVIATE[Weaviate]
            PGVECTOR[PGVector]
            CHROMA[ChromaDB]
        end
        
        subgraph "Graph Databases"
            KUZU[Kuzu<br/>Default]
            NEO4J[Neo4j]
            MEMGRAPH[Memgraph]
            NEPTUNE[AWS Neptune]
        end
        
        subgraph "Relational Databases"
            SQLITE[SQLite<br/>Default]
            POSTGRES[PostgreSQL]
        end
        
        subgraph "Cache Layer"
            REDIS[Redis]
            MEMORY[In-Memory]
        end
        
        subgraph "Adapter Layer"
            VEC_ADAPTER[Vector Adapter]
            GRAPH_ADAPTER[Graph Adapter]
            REL_ADAPTER[Relational Adapter]
            CACHE_ADAPTER[Cache Adapter]
        end
    end
    
    LANCE --> VEC_ADAPTER
    QDRANT --> VEC_ADAPTER
    WEAVIATE --> VEC_ADAPTER
    PGVECTOR --> VEC_ADAPTER
    CHROMA --> VEC_ADAPTER
    
    KUZU --> GRAPH_ADAPTER
    NEO4J --> GRAPH_ADAPTER
    MEMGRAPH --> GRAPH_ADAPTER
    NEPTUNE --> GRAPH_ADAPTER
    
    SQLITE --> REL_ADAPTER
    POSTGRES --> REL_ADAPTER
    
    REDIS --> CACHE_ADAPTER
    MEMORY --> CACHE_ADAPTER
    
    VEC_ADAPTER --> |Embeddings| APP[Application Layer]
    GRAPH_ADAPTER --> |Knowledge Graph| APP
    REL_ADAPTER --> |Metadata| APP
    CACHE_ADAPTER --> |Performance| APP
    
    style LANCE fill:#c7ecee
    style KUZU fill:#d4a5a5
    style SQLITE fill:#ffd3b6
    style VEC_ADAPTER fill:#a8e6cf
    style GRAPH_ADAPTER fill:#ffaaa5
    style REL_ADAPTER fill:#ff8b94
```

**Description:** Cognee uses a multi-database strategy where vector databases store embeddings for semantic search, graph databases store knowledge relationships, and relational databases manage metadata and user information.

---

## 6. API Layer Architecture

RESTful API structure and endpoint organization.

```mermaid
graph TB
    subgraph "API v1 Structure"
        ROOT[/api/v1/]
        
        subgraph "Core Operations"
            ADD[/add<br/>POST - Add data]
            COGNIFY[/cognify<br/>POST - Process data]
            SEARCH[/search<br/>POST - Query]
            PRUNE[/prune<br/>DELETE - Clean]
        end
        
        subgraph "Resource Management"
            DATASETS[/datasets<br/>GET, POST, DELETE]
            CONFIG[/config<br/>GET, PUT]
            UPDATE[/update<br/>PUT]
        end
        
        subgraph "Advanced Features"
            VISUALIZE[/visualize<br/>GET - Graph viz]
            RESPONSES[/responses<br/>Tool responses]
            CLOUD[/cloud<br/>Cloud sync]
        end
        
        subgraph "System"
            HEALTH[/health<br/>GET - Health check]
            UI[/ui<br/>Start UI server]
        end
    end
    
    ROOT --> ADD
    ROOT --> COGNIFY
    ROOT --> SEARCH
    ROOT --> PRUNE
    ROOT --> DATASETS
    ROOT --> CONFIG
    ROOT --> UPDATE
    ROOT --> VISUALIZE
    ROOT --> RESPONSES
    ROOT --> CLOUD
    ROOT --> HEALTH
    ROOT --> UI
    
    ADD --> |Uses| PIPELINE_SVC[Pipeline Service]
    COGNIFY --> |Uses| PIPELINE_SVC
    SEARCH --> |Uses| SEARCH_SVC[Search Service]
    DATASETS --> |Uses| DATA_SVC[Data Service]
    
    PIPELINE_SVC --> TASKS[Task Execution]
    SEARCH_SVC --> RETRIEVERS[Retrievers]
    DATA_SVC --> DB[Database]
    
    style ADD fill:#a8e6cf
    style COGNIFY fill:#ffd3b6
    style SEARCH fill:#ff8b94
    style DATASETS fill:#c7ecee
```

**Description:** The API layer follows RESTful conventions and provides a clean interface for all Cognee operations, from data ingestion to search and visualization.

---

## 7. Pipeline Processing System

The pipeline system orchestrates task execution and data flow.

```mermaid
graph TB
    subgraph "Pipeline System"
        subgraph "Pipeline Core"
            PIPELINE[Pipeline Orchestrator]
            TASK_RUNNER[Task Runner]
            PARALLEL[Parallel Executor]
            SEQUENTIAL[Sequential Executor]
        end
        
        subgraph "Pipeline Models"
            PIPELINE_MODEL[Pipeline Model]
            PIPELINE_RUN[Pipeline Run]
            TASK_MODEL[Task Model]
            TASK_RUN[Task Run]
            DATA_STATUS[Data Item Status]
        end
        
        subgraph "Pipeline Layers"
            AUTH_LAYER[Authorization Layer]
            VALIDATION_LAYER[Validation Layer]
            SETUP_LAYER[Setup Layer]
            EXEC_MODE[Execution Mode Layer]
            RESET_LAYER[Reset Status Layer]
        end
        
        subgraph "Task Types"
            DOC_TASK[Document Tasks]
            GRAPH_TASK[Graph Tasks]
            STORAGE_TASK[Storage Tasks]
            SUMM_TASK[Summary Tasks]
            ENTITY_TASK[Entity Tasks]
        end
    end
    
    PIPELINE --> AUTH_LAYER
    AUTH_LAYER --> VALIDATION_LAYER
    VALIDATION_LAYER --> SETUP_LAYER
    SETUP_LAYER --> EXEC_MODE
    EXEC_MODE --> TASK_RUNNER
    
    TASK_RUNNER --> PARALLEL
    TASK_RUNNER --> SEQUENTIAL
    
    PARALLEL --> DOC_TASK
    PARALLEL --> GRAPH_TASK
    PARALLEL --> STORAGE_TASK
    SEQUENTIAL --> SUMM_TASK
    SEQUENTIAL --> ENTITY_TASK
    
    PIPELINE --> PIPELINE_MODEL
    TASK_RUNNER --> TASK_MODEL
    PIPELINE_RUN --> TASK_RUN
    TASK_RUN --> DATA_STATUS
    
    style PIPELINE fill:#a8e6cf
    style TASK_RUNNER fill:#ffd3b6
    style PARALLEL fill:#ffaaa5
    style SEQUENTIAL fill:#ff8b94
```

**Description:** The pipeline system provides flexible task orchestration with support for parallel and sequential execution, comprehensive status tracking, and error handling.

---

## 8. Module Dependencies

Dependencies between major modules showing information flow.

```mermaid
graph LR
    subgraph "User-Facing Modules"
        API_MOD[API Module]
        CLI_MOD[CLI Module]
    end
    
    subgraph "Core Processing Modules"
        PIPELINE_MOD[Pipelines Module]
        COGNIFY_MODUL[Cognify Module]
        MEMIFY_MODUL[Memify Module]
        SEARCH_MODUL[Search Module]
    end
    
    subgraph "Feature Modules"
        CHUNKING_MOD[Chunking Module]
        RETRIEVAL_MOD[Retrieval Module]
        ONTOLOGY_MOD[Ontology Module]
        USERS_MOD[Users Module]
        DATA_MOD[Data Module]
        STORAGE_MOD[Storage Module]
        VISUALIZATION_MOD[Visualization Module]
        OBSERVABILITY_MOD[Observability Module]
    end
    
    subgraph "Infrastructure Modules"
        LLM_MOD[LLM Module]
        DB_MOD[Database Module]
        FILE_MOD[Files Module]
        LOADER_MOD[Loaders Module]
        ENGINE_MOD[Engine Module]
    end
    
    API_MOD --> PIPELINE_MOD
    CLI_MOD --> PIPELINE_MOD
    
    PIPELINE_MOD --> COGNIFY_MODUL
    PIPELINE_MOD --> MEMIFY_MODUL
    COGNIFY_MODUL --> CHUNKING_MOD
    COGNIFY_MODUL --> ONTOLOGY_MOD
    MEMIFY_MODUL --> RETRIEVAL_MOD
    SEARCH_MODUL --> RETRIEVAL_MOD
    
    COGNIFY_MODUL --> LLM_MOD
    SEARCH_MODUL --> LLM_MOD
    MEMIFY_MODUL --> LLM_MOD
    
    RETRIEVAL_MOD --> DB_MOD
    CHUNKING_MOD --> DB_MOD
    STORAGE_MOD --> DB_MOD
    
    PIPELINE_MOD --> USERS_MOD
    PIPELINE_MOD --> DATA_MOD
    DATA_MOD --> FILE_MOD
    
    DB_MOD --> ENGINE_MOD
    
    PIPELINE_MOD --> OBSERVABILITY_MOD
    SEARCH_MODUL --> VISUALIZATION_MOD
    
    style API_MOD fill:#e1f5ff
    style PIPELINE_MOD fill:#fff9e1
    style LLM_MOD fill:#ffe1f5
    style DB_MOD fill:#e1ffe1
```

**Description:** This dependency graph shows how modules interact, with clear separation of concerns between user interfaces, processing logic, feature modules, and infrastructure.

---

## 9. Data Flow - Add Operation

Detailed data flow for the add/ingestion operation.

```mermaid
flowchart TD
    START([User calls cognee.add]) --> VALIDATE{Validate Input}
    VALIDATE -->|Valid| AUTH[Authenticate User]
    VALIDATE -->|Invalid| ERROR1[Raise ValueError]
    
    AUTH --> DATASET[Resolve/Create Dataset]
    DATASET --> PERMS[Grant Permissions]
    PERMS --> TYPE{Determine Data Type}
    
    TYPE -->|Text String| DIRECT[Direct Text Storage]
    TYPE -->|File Path| FILE_LOAD[Load from File System]
    TYPE -->|S3 Path| S3_LOAD[Load from S3]
    TYPE -->|URL| URL_LOAD[Fetch from URL]
    TYPE -->|Binary Stream| STREAM_LOAD[Read Stream]
    
    FILE_LOAD --> EXTRACT[Extract Content]
    S3_LOAD --> EXTRACT
    URL_LOAD --> EXTRACT
    STREAM_LOAD --> EXTRACT
    DIRECT --> EXTRACT
    
    EXTRACT --> LOADER{Select Loader}
    LOADER -->|PDF| PDF_LOADER[PDF Loader]
    LOADER -->|Image| IMG_LOADER[Image OCR Loader]
    LOADER -->|Audio| AUDIO_LOADER[Audio Transcription]
    LOADER -->|Code| CODE_LOADER[Code Parser]
    LOADER -->|Text| TEXT_LOADER[Text Loader]
    
    PDF_LOADER --> STORE[Store in Relational DB]
    IMG_LOADER --> STORE
    AUDIO_LOADER --> STORE
    CODE_LOADER --> STORE
    TEXT_LOADER --> STORE
    
    STORE --> FILE_STORE[Save to File Storage]
    FILE_STORE --> META[Update Metadata]
    META --> STATUS[Update Pipeline Status]
    STATUS --> END([Return PipelineRunInfo])
    
    ERROR1 --> END
    
    style START fill:#a8e6cf
    style EXTRACT fill:#ffd3b6
    style STORE fill:#ffaaa5
    style END fill:#ff8b94
```

**Description:** The add operation handles multiple data formats, automatically selecting the appropriate loader and extraction strategy, then storing the content with proper metadata and permissions.

---

## 10. Data Flow - Cognify Operation

Detailed data flow for the cognify/processing operation.

```mermaid
flowchart TD
    START([User calls cognee.cognify]) --> AUTH[Authenticate User]
    AUTH --> RESOLVE[Resolve Datasets]
    RESOLVE --> PERM_CHECK{Check Permissions}
    
    PERM_CHECK -->|Authorized| CLASSIFY[Classify Documents]
    PERM_CHECK -->|Unauthorized| ERROR1[Raise PermissionError]
    
    CLASSIFY --> CHUNK[Chunk Text]
    CHUNK --> CONFIG{Chunking Strategy}
    
    CONFIG -->|Fixed Size| FIXED[Fixed Size Chunking]
    CONFIG -->|Semantic| SEMANTIC[Semantic Chunking]
    CONFIG -->|Custom| CUSTOM[Custom Chunker]
    
    FIXED --> EMBED[Generate Embeddings]
    SEMANTIC --> EMBED
    CUSTOM --> EMBED
    
    EMBED --> VEC_STORE[Store in Vector DB]
    VEC_STORE --> EXTRACT_ENT[Extract Entities]
    
    EXTRACT_ENT --> LLM_CALL[LLM API Call]
    LLM_CALL --> ONTOLOGY{Apply Ontology?}
    
    ONTOLOGY -->|Yes| ONTOLOGY_MAP[Map to Ontology]
    ONTOLOGY -->|No| BUILD_GRAPH[Build Knowledge Graph]
    ONTOLOGY_MAP --> BUILD_GRAPH
    
    BUILD_GRAPH --> GRAPH_STORE[Store in Graph DB]
    GRAPH_STORE --> REL_EXTRACT[Extract Relationships]
    REL_EXTRACT --> REL_STORE[Store Relationships]
    
    REL_STORE --> SUMMARIZE[Generate Summaries]
    SUMMARIZE --> SUM_STORE[Store Summaries]
    SUM_STORE --> TEMPORAL{Temporal Analysis?}
    
    TEMPORAL -->|Yes| TEMP_EXTRACT[Extract Events/Time]
    TEMPORAL -->|No| UPDATE_STATUS[Update Pipeline Status]
    TEMP_EXTRACT --> TEMP_STORE[Store Temporal Data]
    TEMP_STORE --> UPDATE_STATUS
    
    UPDATE_STATUS --> END([Return Success])
    ERROR1 --> END
    
    style START fill:#a8e6cf
    style EMBED fill:#ffd3b6
    style BUILD_GRAPH fill:#ffaaa5
    style END fill:#ff8b94
```

**Description:** The cognify operation transforms raw text into a structured knowledge graph through chunking, entity extraction, relationship detection, and semantic indexing.

---

## 11. Data Flow - Memify Operation

Detailed data flow for the memify/enrichment operation.

```mermaid
flowchart TD
    START([User calls cognee.memify]) --> AUTH[Authenticate User]
    AUTH --> RESOLVE[Resolve Dataset]
    RESOLVE --> CHECK_DATA{Data Provided?}
    
    CHECK_DATA -->|No| EXTRACT_SUBGRAPH[Extract Subgraph from Graph DB]
    CHECK_DATA -->|Yes| USE_DATA[Use Provided Data]
    
    EXTRACT_SUBGRAPH --> FILTER{Filter Options?}
    FILTER -->|Node Type| FILTER_TYPE[Filter by Node Type]
    FILTER -->|Node Name| FILTER_NAME[Filter by Node Name]
    FILTER -->|None| FULL_GRAPH[Use Full Graph]
    
    FILTER_TYPE --> PREPARE[Prepare Memory Fragment]
    FILTER_NAME --> PREPARE
    FULL_GRAPH --> PREPARE
    USE_DATA --> PREPARE
    
    PREPARE --> EXTRACTION{Extraction Tasks}
    EXTRACTION --> CUSTOM_EXTRACT[Run Custom Extractors]
    CUSTOM_EXTRACT --> DEFAULT_EXTRACT[Run Default Extractors]
    
    DEFAULT_EXTRACT --> SUBGRAPH_CHUNKS[Extract Subgraph Chunks]
    SUBGRAPH_CHUNKS --> ENRICHMENT{Enrichment Tasks}
    
    ENRICHMENT --> RULES[Apply Coding Rules]
    RULES --> ASSOCIATIONS[Add Rule Associations]
    ASSOCIATIONS --> CUSTOM_ENRICH[Run Custom Enrichments]
    
    CUSTOM_ENRICH --> UPDATE_GRAPH[Update Graph with Enrichments]
    UPDATE_GRAPH --> STORE[Store Enhanced Relationships]
    STORE --> UPDATE_STATUS[Update Pipeline Status]
    UPDATE_STATUS --> END([Return Success])
    
    style START fill:#a8e6cf
    style EXTRACT_SUBGRAPH fill:#ffd3b6
    style ENRICHMENT fill:#ffaaa5
    style END fill:#ff8b94
```

**Description:** The memify operation enriches existing knowledge graphs with memory algorithms, rules, and custom processing to enhance the graph's intelligence and reasoning capabilities.

---

## 12. Data Flow - Search Operation

Detailed data flow for the search/query operation.

```mermaid
flowchart TD
    START([User calls cognee.search]) --> AUTH[Authenticate User]
    AUTH --> RESOLVE[Resolve Datasets]
    RESOLVE --> TYPE{Query Type}
    
    TYPE -->|GRAPH_COMPLETION| GRAPH_COMP[Graph Completion]
    TYPE -->|RAG_COMPLETION| RAG_COMP[RAG Completion]
    TYPE -->|CHUNKS| CHUNKS_SEARCH[Chunk Search]
    TYPE -->|SUMMARIES| SUM_SEARCH[Summary Search]
    TYPE -->|CODE| CODE_SEARCH[Code Search]
    TYPE -->|CYPHER| CYPHER_SEARCH[Cypher Query]
    TYPE -->|FEELING_LUCKY| AUTO_SELECT[Auto-Select Type]
    TYPE -->|CHUNKS_LEXICAL| LEX_SEARCH[Lexical Search]
    
    GRAPH_COMP --> VEC_SEARCH[Vector Similarity Search]
    RAG_COMP --> VEC_SEARCH
    CHUNKS_SEARCH --> VEC_SEARCH
    LEX_SEARCH --> LEXICAL[Jaccard/Token Search]
    
    VEC_SEARCH --> TOP_K[Get Top-K Results]
    LEXICAL --> TOP_K
    TOP_K --> GRAPH_TRAV[Graph Traversal]
    
    GRAPH_TRAV --> CONTEXT[Build Context]
    CONTEXT --> SYS_PROMPT[Load System Prompt]
    SYS_PROMPT --> LLM_GEN[LLM Generation]
    LLM_GEN --> ANSWER[Generate Answer]
    
    SUM_SEARCH --> RETRIEVE_SUM[Retrieve Summaries]
    RETRIEVE_SUM --> ANSWER
    
    CODE_SEARCH --> CODE_RETR[Code-Specific Retrieval]
    CODE_RETR --> ANSWER
    
    CYPHER_SEARCH --> EXEC_CYPHER[Execute Cypher]
    EXEC_CYPHER --> ANSWER
    
    AUTO_SELECT --> ANALYZE[Analyze Query]
    ANALYZE --> SELECT_BEST[Select Best Method]
    SELECT_BEST --> VEC_SEARCH
    
    ANSWER --> SAVE{Save Interaction?}
    SAVE -->|Yes| SAVE_HISTORY[Save to History]
    SAVE -->|No| FORMAT[Format Results]
    SAVE_HISTORY --> FORMAT
    
    FORMAT --> END([Return Results])
    
    style START fill:#a8e6cf
    style VEC_SEARCH fill:#ffd3b6
    style LLM_GEN fill:#ffaaa5
    style END fill:#ff8b94
```

**Description:** The search operation provides multiple retrieval strategies, from simple vector search to complex graph traversal with LLM-powered reasoning, automatically adapting to the query type.

---

## 13. LLM Integration Architecture

How Cognee integrates with various LLM providers.

```mermaid
graph TB
    subgraph "LLM Gateway"
        GATEWAY[LLM Gateway]
        
        subgraph "Provider Support via LiteLLM"
            OPENAI[OpenAI]
            ANTHROPIC[Anthropic]
            GOOGLE[Google Gemini]
            AZURE[Azure OpenAI]
            MISTRAL[Mistral AI]
            BEDROCK[AWS Bedrock]
            OLLAMA[Ollama<br/>Local Models]
            CUSTOM[Custom Providers]
        end
        
        subgraph "LLM Features"
            GENERATION[Text Generation]
            STRUCTURED_OUT[Structured Output]
            EMBEDDINGS[Embeddings]
            STREAMING[Streaming]
            FUNCTION_CALL[Function Calling]
        end
        
        subgraph "LLM Utilities"
            TOKENIZER_UTIL[Tokenizer]
            PROMPT_MGMT[Prompt Management]
            RETRY_LOGIC[Retry Logic]
            RATE_LIMIT[Rate Limiting]
            COST_TRACK[Cost Tracking]
        end
    end
    
    GATEWAY --> OPENAI
    GATEWAY --> ANTHROPIC
    GATEWAY --> GOOGLE
    GATEWAY --> AZURE
    GATEWAY --> MISTRAL
    GATEWAY --> BEDROCK
    GATEWAY --> OLLAMA
    GATEWAY --> CUSTOM
    
    GATEWAY --> GENERATION
    GATEWAY --> STRUCTURED_OUT
    GATEWAY --> EMBEDDINGS
    GATEWAY --> STREAMING
    GATEWAY --> FUNCTION_CALL
    
    GENERATION --> TOKENIZER_UTIL
    STRUCTURED_OUT --> PROMPT_MGMT
    EMBEDDINGS --> RETRY_LOGIC
    STREAMING --> RATE_LIMIT
    FUNCTION_CALL --> COST_TRACK
    
    PROMPT_MGMT --> TEMPLATES[Prompt Templates<br/>Jinja2]
    
    style GATEWAY fill:#a8e6cf
    style STRUCTURED_OUT fill:#ffd3b6
    style PROMPT_MGMT fill:#ffaaa5
```

**Description:** The LLM Gateway provides a unified interface to multiple LLM providers through LiteLLM, supporting advanced features like structured outputs, streaming, and function calling while handling rate limiting and retries.

---

## 14. Vector Database Integration

Vector database architecture for semantic search.

```mermaid
graph TB
    subgraph "Vector Database Layer"
        VEC_ENGINE[Vector Engine]
        
        subgraph "Supported Vector DBs"
            LANCE_VEC[LanceDB<br/>Default, Local]
            QDRANT_VEC[Qdrant<br/>Cloud/Local]
            WEAVIATE_VEC[Weaviate<br/>Cloud/Local]
            PG_VEC[PGVector<br/>PostgreSQL Extension]
            CHROMA_VEC[ChromaDB<br/>Local]
        end
        
        subgraph "Vector Operations"
            CREATE_COL[Create Collection]
            INSERT_VEC[Insert Vectors]
            SEARCH_VEC[Similarity Search]
            DELETE_VEC[Delete Vectors]
            UPDATE_VEC[Update Metadata]
            HYBRID_SEARCH[Hybrid Search]
        end
        
        subgraph "Embedding Models"
            OPENAI_EMB[OpenAI<br/>text-embedding-3]
            FASTEMBED[FastEmbed<br/>Local Models]
            CUSTOM_EMB[Custom Models]
        end
        
        subgraph "Search Strategies"
            COSINE[Cosine Similarity]
            EUCLIDEAN[Euclidean Distance]
            DOT_PRODUCT[Dot Product]
        end
    end
    
    VEC_ENGINE --> LANCE_VEC
    VEC_ENGINE --> QDRANT_VEC
    VEC_ENGINE --> WEAVIATE_VEC
    VEC_ENGINE --> PG_VEC
    VEC_ENGINE --> CHROMA_VEC
    
    VEC_ENGINE --> CREATE_COL
    VEC_ENGINE --> INSERT_VEC
    VEC_ENGINE --> SEARCH_VEC
    VEC_ENGINE --> DELETE_VEC
    VEC_ENGINE --> UPDATE_VEC
    VEC_ENGINE --> HYBRID_SEARCH
    
    INSERT_VEC --> OPENAI_EMB
    INSERT_VEC --> FASTEMBED
    INSERT_VEC --> CUSTOM_EMB
    
    SEARCH_VEC --> COSINE
    SEARCH_VEC --> EUCLIDEAN
    SEARCH_VEC --> DOT_PRODUCT
    
    style VEC_ENGINE fill:#a8e6cf
    style LANCE_VEC fill:#c7ecee
    style SEARCH_VEC fill:#ffd3b6
    style OPENAI_EMB fill:#ffaaa5
```

**Description:** Vector databases store embeddings for semantic search, with LanceDB as the default for its efficiency and local-first approach. Multiple providers are supported for different deployment scenarios.

---

## 15. Graph Database Integration

Graph database architecture for knowledge representation.

```mermaid
graph TB
    subgraph "Graph Database Layer"
        GRAPH_ENGINE[Graph Engine]
        
        subgraph "Supported Graph DBs"
            KUZU_GRAPH[Kuzu<br/>Default, Embedded]
            NEO4J_GRAPH[Neo4j<br/>Enterprise]
            MEMGRAPH_GRAPH[Memgraph<br/>High Performance]
            NEPTUNE_GRAPH[AWS Neptune<br/>Cloud]
        end
        
        subgraph "Graph Operations"
            CREATE_NODE[Create Nodes]
            CREATE_EDGE[Create Edges]
            QUERY_GRAPH[Query Graph]
            TRAVERSE[Traverse Path]
            SUBGRAPH[Extract Subgraph]
            UPDATE_PROPS[Update Properties]
            DELETE_NODE[Delete Nodes/Edges]
        end
        
        subgraph "Graph Models"
            ENTITY[Entity Nodes]
            RELATION[Relationship Edges]
            NODESET[Node Sets]
            TEMPORAL[Temporal Data]
            PROPERTIES[Node Properties]
        end
        
        subgraph "Query Languages"
            CYPHER[Cypher Queries]
            GRAPH_API[Graph API]
            PATTERN_MATCH[Pattern Matching]
        end
    end
    
    GRAPH_ENGINE --> KUZU_GRAPH
    GRAPH_ENGINE --> NEO4J_GRAPH
    GRAPH_ENGINE --> MEMGRAPH_GRAPH
    GRAPH_ENGINE --> NEPTUNE_GRAPH
    
    GRAPH_ENGINE --> CREATE_NODE
    GRAPH_ENGINE --> CREATE_EDGE
    GRAPH_ENGINE --> QUERY_GRAPH
    GRAPH_ENGINE --> TRAVERSE
    GRAPH_ENGINE --> SUBGRAPH
    GRAPH_ENGINE --> UPDATE_PROPS
    GRAPH_ENGINE --> DELETE_NODE
    
    CREATE_NODE --> ENTITY
    CREATE_EDGE --> RELATION
    CREATE_NODE --> NODESET
    ENTITY --> TEMPORAL
    ENTITY --> PROPERTIES
    
    QUERY_GRAPH --> CYPHER
    QUERY_GRAPH --> GRAPH_API
    TRAVERSE --> PATTERN_MATCH
    
    style GRAPH_ENGINE fill:#a8e6cf
    style KUZU_GRAPH fill:#d4a5a5
    style QUERY_GRAPH fill:#ffd3b6
    style CYPHER fill:#ffaaa5
```

**Description:** Graph databases store the knowledge graph structure with nodes representing entities and edges representing relationships. Kuzu is the default for its embedded nature and high performance.

---

## 16. Task System Architecture

Task-based processing architecture for modular operations.

```mermaid
graph TB
    subgraph "Task System"
        TASK_BASE[Task Base Class]
        
        subgraph "Document Tasks"
            CLASSIFY_DOC[Classify Documents]
            EXTRACT_CHUNKS[Extract Chunks]
            CHECK_PERMS[Check Permissions]
        end
        
        subgraph "Graph Tasks"
            EXTRACT_GRAPH[Extract Graph from Data]
            BUILD_GRAPH[Build Knowledge Graph]
            UPDATE_GRAPH[Update Graph]
        end
        
        subgraph "Storage Tasks"
            ADD_DATA_POINTS[Add Data Points]
            STORE_EMBED[Store Embeddings]
            SAVE_META[Save Metadata]
        end
        
        subgraph "Summarization Tasks"
            SUMMARIZE_TEXT[Summarize Text]
            MULTI_LEVEL[Multi-Level Summaries]
            STORE_SUMMARIES[Store Summaries]
        end
        
        subgraph "Entity Tasks"
            EXTRACT_ENTITIES[Extract Entities]
            ENTITY_RESOLVE[Entity Resolution]
            ENTITY_LINK[Entity Linking]
        end
        
        subgraph "Temporal Tasks"
            EXTRACT_EVENTS[Extract Events]
            EXTRACT_TIME[Extract Timestamps]
            BUILD_TEMPORAL[Build Temporal Graph]
        end
        
        subgraph "Code Tasks"
            PARSE_CODE[Parse Code]
            EXTRACT_SYMBOLS[Extract Symbols]
            BUILD_CODE_GRAPH[Build Code Graph]
        end
        
        subgraph "Memify Tasks"
            EXTRACT_SUBGRAPH[Extract Subgraph Chunks]
            ADD_RULES[Add Rule Associations]
            ENRICH_GRAPH[Enrich Graph]
        end
    end
    
    TASK_BASE --> CLASSIFY_DOC
    TASK_BASE --> EXTRACT_CHUNKS
    TASK_BASE --> CHECK_PERMS
    TASK_BASE --> EXTRACT_GRAPH
    TASK_BASE --> BUILD_GRAPH
    TASK_BASE --> UPDATE_GRAPH
    TASK_BASE --> ADD_DATA_POINTS
    TASK_BASE --> STORE_EMBED
    TASK_BASE --> SAVE_META
    TASK_BASE --> SUMMARIZE_TEXT
    TASK_BASE --> MULTI_LEVEL
    TASK_BASE --> STORE_SUMMARIES
    TASK_BASE --> EXTRACT_ENTITIES
    TASK_BASE --> ENTITY_RESOLVE
    TASK_BASE --> ENTITY_LINK
    TASK_BASE --> EXTRACT_EVENTS
    TASK_BASE --> EXTRACT_TIME
    TASK_BASE --> BUILD_TEMPORAL
    TASK_BASE --> PARSE_CODE
    TASK_BASE --> EXTRACT_SYMBOLS
    TASK_BASE --> BUILD_CODE_GRAPH
    TASK_BASE --> EXTRACT_SUBGRAPH
    TASK_BASE --> ADD_RULES
    TASK_BASE --> ENRICH_GRAPH
    
    style TASK_BASE fill:#a8e6cf
    style EXTRACT_GRAPH fill:#ffd3b6
    style SUMMARIZE_TEXT fill:#ffaaa5
    style EXTRACT_ENTITIES fill:#ff8b94
```

**Description:** Tasks are modular processing units that can be composed into pipelines. Each task handles a specific operation in the ECL workflow, from document classification to graph enrichment.

---

## 17. Chunking Strategy

Text chunking approaches for optimal processing.

```mermaid
graph TB
    subgraph "Chunking System"
        CHUNKER[Chunker Interface]
        
        subgraph "Chunking Strategies"
            TEXT_CHUNKER[TextChunker<br/>Fixed Size]
            SEMANTIC_CHUNKER[Semantic Chunker<br/>Meaning-based]
            LANGCHAIN_CHUNKER[LangChain Chunker<br/>Advanced]
            CUSTOM_CHUNKER[Custom Chunker<br/>Domain-specific]
        end
        
        subgraph "Chunking Parameters"
            CHUNK_SIZE[Chunk Size<br/>Token count]
            OVERLAP[Overlap<br/>Context preservation]
            SEPARATORS[Separators<br/>Split points]
            MAX_TOKENS[Max Tokens<br/>LLM limits]
        end
        
        subgraph "Post-Processing"
            CLEAN[Clean Text]
            NORMALIZE[Normalize]
            METADATA[Add Metadata]
            INDEX[Assign Index]
        end
        
        subgraph "Output"
            CHUNKS[Text Chunks]
            CHUNK_META[Chunk Metadata]
            RELATIONSHIPS[Chunk Relationships]
        end
    end
    
    CHUNKER --> TEXT_CHUNKER
    CHUNKER --> SEMANTIC_CHUNKER
    CHUNKER --> LANGCHAIN_CHUNKER
    CHUNKER --> CUSTOM_CHUNKER
    
    TEXT_CHUNKER --> CHUNK_SIZE
    TEXT_CHUNKER --> OVERLAP
    SEMANTIC_CHUNKER --> SEPARATORS
    LANGCHAIN_CHUNKER --> MAX_TOKENS
    
    CHUNK_SIZE --> CLEAN
    OVERLAP --> CLEAN
    SEPARATORS --> NORMALIZE
    MAX_TOKENS --> METADATA
    
    CLEAN --> CHUNKS
    NORMALIZE --> CHUNKS
    METADATA --> CHUNK_META
    INDEX --> RELATIONSHIPS
    
    style CHUNKER fill:#a8e6cf
    style TEXT_CHUNKER fill:#ffd3b6
    style CLEAN fill:#ffaaa5
    style CHUNKS fill:#ff8b94
```

**Description:** Chunking breaks down large documents into manageable pieces for LLM processing. Multiple strategies are available, from simple fixed-size splitting to sophisticated semantic chunking that preserves meaning.

---

## 18. Retrieval System

Multi-modal retrieval system for information access.

```mermaid
graph TB
    subgraph "Retrieval System"
        BASE_RETRIEVER[Base Retriever]
        
        subgraph "Retrieval Strategies"
            CHUNKS_RETR[Chunks Retriever<br/>Raw text segments]
            GRAPH_RETR[Graph Completion<br/>Graph-based reasoning]
            RAG_RETR[Completion Retriever<br/>Traditional RAG]
            SUMMARIES_RETR[Summaries Retriever<br/>Pre-generated summaries]
            CODE_RETR[Code Retriever<br/>Code-specific]
            CYPHER_RETR[Cypher Search<br/>Direct queries]
            TEMPORAL_RETR[Temporal Retriever<br/>Time-aware]
            LEXICAL_RETR[Lexical Retriever<br/>Token-based]
            HYBRID_RETR[Hybrid Retriever<br/>Combined methods]
        end
        
        subgraph "Context Providers"
            ENTITY_CTX[Entity Context]
            RELATION_CTX[Relationship Context]
            SUMMARY_CTX[Summary Context]
            TEMPORAL_CTX[Temporal Context]
        end
        
        subgraph "Retrieval Components"
            VEC_SEARCH_COMP[Vector Search]
            GRAPH_TRAV_COMP[Graph Traversal]
            RERANK[Re-ranking]
            FILTER[Filtering]
        end
    end
    
    BASE_RETRIEVER --> CHUNKS_RETR
    BASE_RETRIEVER --> GRAPH_RETR
    BASE_RETRIEVER --> RAG_RETR
    BASE_RETRIEVER --> SUMMARIES_RETR
    BASE_RETRIEVER --> CODE_RETR
    BASE_RETRIEVER --> CYPHER_RETR
    BASE_RETRIEVER --> TEMPORAL_RETR
    BASE_RETRIEVER --> LEXICAL_RETR
    BASE_RETRIEVER --> HYBRID_RETR
    
    GRAPH_RETR --> ENTITY_CTX
    GRAPH_RETR --> RELATION_CTX
    SUMMARIES_RETR --> SUMMARY_CTX
    TEMPORAL_RETR --> TEMPORAL_CTX
    
    CHUNKS_RETR --> VEC_SEARCH_COMP
    GRAPH_RETR --> GRAPH_TRAV_COMP
    RAG_RETR --> VEC_SEARCH_COMP
    
    VEC_SEARCH_COMP --> RERANK
    GRAPH_TRAV_COMP --> RERANK
    RERANK --> FILTER
    
    style BASE_RETRIEVER fill:#a8e6cf
    style GRAPH_RETR fill:#ffd3b6
    style HYBRID_RETR fill:#ffaaa5
    style RERANK fill:#ff8b94
```

**Description:** The retrieval system provides multiple strategies for information access, from simple chunk retrieval to sophisticated graph-based reasoning, with support for hybrid approaches.

---

## 19. Knowledge Graph Construction

How Cognee builds and maintains knowledge graphs.

```mermaid
flowchart TD
    START[Input: Text Chunks] --> EXTRACT_ENT[Extract Entities]
    EXTRACT_ENT --> LLM_ENT[LLM: Entity Extraction]
    LLM_ENT --> ENTITY_LIST[Entity List]
    
    ENTITY_LIST --> ONTOLOGY_CHECK{Apply Ontology?}
    ONTOLOGY_CHECK -->|Yes| MAP_ONTOLOGY[Map to Ontology Classes]
    ONTOLOGY_CHECK -->|No| CREATE_NODES[Create Entity Nodes]
    MAP_ONTOLOGY --> CREATE_NODES
    
    CREATE_NODES --> DEDUPE[Deduplicate Entities]
    DEDUPE --> RESOLVE[Entity Resolution]
    RESOLVE --> STORE_NODES[Store Nodes in Graph DB]
    
    ENTITY_LIST --> EXTRACT_REL[Extract Relationships]
    EXTRACT_REL --> LLM_REL[LLM: Relationship Extraction]
    LLM_REL --> REL_LIST[Relationship List]
    
    REL_LIST --> VALIDATE_REL[Validate Relationships]
    VALIDATE_REL --> CREATE_EDGES[Create Edges]
    CREATE_EDGES --> STORE_EDGES[Store Edges in Graph DB]
    
    STORE_NODES --> EMBED_NODES[Generate Node Embeddings]
    EMBED_NODES --> STORE_VEC[Store in Vector DB]
    
    STORE_EDGES --> COMPUTE_PROPS[Compute Properties]
    COMPUTE_PROPS --> WEIGHT[Calculate Edge Weights]
    WEIGHT --> TEMPORAL_INFO{Temporal Info?}
    
    TEMPORAL_INFO -->|Yes| ADD_TEMPORAL[Add Temporal Attributes]
    TEMPORAL_INFO -->|No| FINALIZE[Finalize Graph]
    ADD_TEMPORAL --> FINALIZE
    
    STORE_VEC --> FINALIZE
    FINALIZE --> OUTPUT[Output: Knowledge Graph]
    
    style START fill:#a8e6cf
    style LLM_ENT fill:#ffd3b6
    style CREATE_NODES fill:#ffaaa5
    style OUTPUT fill:#ff8b94
```

**Description:** Knowledge graph construction involves entity extraction, relationship detection, deduplication, and semantic embedding, creating a rich network of interconnected concepts.

---

## 20. Authentication & Permissions

User authentication and permission management system.

```mermaid
graph TB
    subgraph "Authentication System"
        AUTH_MGR[Authentication Manager]
        
        subgraph "User Management"
            USER_MODEL[User Model]
            DEFAULT_USER[Default User]
            CREATE_USER[Create User]
            GET_USER[Get User]
        end
        
        subgraph "Permission System"
            PERM_MODEL[Permission Model]
            DATASET_PERMS[Dataset Permissions]
            NODESET_PERMS[NodeSet Permissions]
            OPERATION_PERMS[Operation Permissions]
        end
        
        subgraph "Permission Types"
            READ[Read Permission]
            WRITE[Write Permission]
            DELETE[Delete Permission]
            SHARE[Share Permission]
        end
        
        subgraph "Access Control"
            CHECK_PERM[Check Permissions]
            GRANT_PERM[Grant Permissions]
            REVOKE_PERM[Revoke Permissions]
            INHERIT_PERM[Inherit Permissions]
        end
        
        subgraph "Context Management"
            USER_CTX[User Context]
            DATASET_CTX[Dataset Context]
            SESSION_CTX[Session Context]
        end
    end
    
    AUTH_MGR --> USER_MODEL
    AUTH_MGR --> DEFAULT_USER
    AUTH_MGR --> CREATE_USER
    AUTH_MGR --> GET_USER
    
    USER_MODEL --> PERM_MODEL
    PERM_MODEL --> DATASET_PERMS
    PERM_MODEL --> NODESET_PERMS
    PERM_MODEL --> OPERATION_PERMS
    
    DATASET_PERMS --> READ
    DATASET_PERMS --> WRITE
    DATASET_PERMS --> DELETE
    DATASET_PERMS --> SHARE
    
    PERM_MODEL --> CHECK_PERM
    PERM_MODEL --> GRANT_PERM
    PERM_MODEL --> REVOKE_PERM
    PERM_MODEL --> INHERIT_PERM
    
    CHECK_PERM --> USER_CTX
    CHECK_PERM --> DATASET_CTX
    CHECK_PERM --> SESSION_CTX
    
    style AUTH_MGR fill:#a8e6cf
    style PERM_MODEL fill:#ffd3b6
    style CHECK_PERM fill:#ffaaa5
```

**Description:** The authentication system manages users and permissions, ensuring secure access to datasets and operations. It supports fine-grained permissions and automatic permission inheritance.

---

## 21. Configuration Management

Configuration system for flexibility and customization.

```mermaid
graph TB
    subgraph "Configuration System"
        CONFIG_MGR[Configuration Manager]
        
        subgraph "Configuration Sources"
            ENV_VARS[Environment Variables<br/>.env file]
            CONFIG_FILE[Configuration File<br/>Python config]
            DEFAULTS[Default Values]
            RUNTIME[Runtime Configuration]
        end
        
        subgraph "Configuration Categories"
            LLM_CONFIG[LLM Configuration<br/>API keys, models]
            DB_CONFIG[Database Configuration<br/>Connections, paths]
            STORAGE_CONFIG[Storage Configuration<br/>File systems, S3]
            PIPELINE_CONFIG[Pipeline Configuration<br/>Tasks, batching]
            LOGGING_CONFIG[Logging Configuration<br/>Levels, formats]
        end
        
        subgraph "Configuration APIs"
            GET_CONFIG[Get Configuration]
            SET_CONFIG[Set Configuration]
            VALIDATE_CONFIG[Validate Configuration]
            RESET_CONFIG[Reset Configuration]
        end
        
        subgraph "Configuration Features"
            TYPE_SAFE[Type Safety<br/>Pydantic]
            VALIDATION[Validation Rules]
            SECRETS[Secret Management]
            OVERRIDE[Override Hierarchy]
        end
    end
    
    CONFIG_MGR --> ENV_VARS
    CONFIG_MGR --> CONFIG_FILE
    CONFIG_MGR --> DEFAULTS
    CONFIG_MGR --> RUNTIME
    
    CONFIG_MGR --> LLM_CONFIG
    CONFIG_MGR --> DB_CONFIG
    CONFIG_MGR --> STORAGE_CONFIG
    CONFIG_MGR --> PIPELINE_CONFIG
    CONFIG_MGR --> LOGGING_CONFIG
    
    CONFIG_MGR --> GET_CONFIG
    CONFIG_MGR --> SET_CONFIG
    CONFIG_MGR --> VALIDATE_CONFIG
    CONFIG_MGR --> RESET_CONFIG
    
    SET_CONFIG --> TYPE_SAFE
    SET_CONFIG --> VALIDATION
    GET_CONFIG --> SECRETS
    RUNTIME --> OVERRIDE
    
    style CONFIG_MGR fill:#a8e6cf
    style ENV_VARS fill:#ffd3b6
    style TYPE_SAFE fill:#ffaaa5
```

**Description:** The configuration system uses Pydantic for type-safe settings, supporting multiple configuration sources with a clear override hierarchy and validation rules.

---

## 22. Observability & Monitoring

Monitoring and observability features for production use.

```mermaid
graph TB
    subgraph "Observability System"
        OBS_MGR[Observability Manager]
        
        subgraph "Logging"
            STRUCT_LOG[Structured Logging<br/>structlog]
            LOG_LEVELS[Log Levels<br/>DEBUG to ERROR]
            LOG_FORMAT[Log Formatting]
            LOG_OUTPUT[Log Output<br/>Console, File]
        end
        
        subgraph "Monitoring Tools"
            LANGFUSE[Langfuse Integration<br/>LLM observability]
            CUSTOM_OBS[Custom Observers]
            NONE_OBS[No Monitoring]
        end
        
        subgraph "Metrics"
            PIPELINE_METRICS[Pipeline Metrics<br/>Status, duration]
            LLM_METRICS[LLM Metrics<br/>Tokens, cost]
            DB_METRICS[Database Metrics<br/>Queries, latency]
            MEMORY_METRICS[Memory Metrics<br/>Usage tracking]
        end
        
        subgraph "Tracing"
            PIPELINE_TRACE[Pipeline Tracing]
            TASK_TRACE[Task Execution]
            DB_TRACE[Database Operations]
            LLM_TRACE[LLM Calls]
        end
        
        subgraph "Error Handling"
            ERROR_CAPTURE[Error Capture]
            ERROR_REPORT[Error Reporting]
            RETRY_TRACK[Retry Tracking]
            ALERT[Alerting]
        end
    end
    
    OBS_MGR --> STRUCT_LOG
    OBS_MGR --> LOG_LEVELS
    OBS_MGR --> LOG_FORMAT
    OBS_MGR --> LOG_OUTPUT
    
    OBS_MGR --> LANGFUSE
    OBS_MGR --> CUSTOM_OBS
    OBS_MGR --> NONE_OBS
    
    OBS_MGR --> PIPELINE_METRICS
    OBS_MGR --> LLM_METRICS
    OBS_MGR --> DB_METRICS
    OBS_MGR --> MEMORY_METRICS
    
    OBS_MGR --> PIPELINE_TRACE
    OBS_MGR --> TASK_TRACE
    OBS_MGR --> DB_TRACE
    OBS_MGR --> LLM_TRACE
    
    OBS_MGR --> ERROR_CAPTURE
    OBS_MGR --> ERROR_REPORT
    OBS_MGR --> RETRY_TRACK
    OBS_MGR --> ALERT
    
    LANGFUSE --> LLM_TRACE
    LANGFUSE --> LLM_METRICS
    
    style OBS_MGR fill:#a8e6cf
    style STRUCT_LOG fill:#ffd3b6
    style LANGFUSE fill:#ffaaa5
    style PIPELINE_TRACE fill:#ff8b94
```

**Description:** Comprehensive observability with structured logging, LLM monitoring via Langfuse, performance metrics, and distributed tracing for debugging and optimization.

---

## 23. Deployment Architecture

Different deployment options for Cognee.

```mermaid
graph TB
    subgraph "Deployment Options"
        subgraph "Local Development"
            LOCAL_DEV[Local Python<br/>SQLite + LanceDB + Kuzu]
            LOCAL_DOCKER[Local Docker<br/>Containerized]
        end
        
        subgraph "Self-Hosted Production"
            VM_DEPLOY[VM/Server<br/>PostgreSQL + Vector + Graph DB]
            K8S_DEPLOY[Kubernetes<br/>Scalable pods]
            DOCKER_COMPOSE[Docker Compose<br/>Multi-container]
        end
        
        subgraph "Cloud Platforms"
            AWS_DEPLOY[AWS<br/>EC2, RDS, S3, Neptune]
            AZURE_DEPLOY[Azure<br/>VM, CosmosDB, Blob]
            GCP_DEPLOY[GCP<br/>Compute, Cloud SQL, Storage]
            MODAL_DEPLOY[Modal<br/>Serverless Python]
        end
        
        subgraph "Hosted Platform"
            COGWIT[Cogwit Platform<br/>Managed Service]
        end
        
        subgraph "Storage Backends"
            LOCAL_STORAGE[Local File System]
            S3_STORAGE[AWS S3]
            AZURE_STORAGE[Azure Blob]
            GCS_STORAGE[Google Cloud Storage]
        end
        
        subgraph "Database Options"
            EMBEDDED[Embedded DBs<br/>SQLite, Kuzu, LanceDB]
            MANAGED[Managed DBs<br/>RDS, Neo4j Cloud, Qdrant Cloud]
            SELF_MANAGED[Self-Managed<br/>PostgreSQL, Neo4j, etc.]
        end
    end
    
    LOCAL_DEV --> LOCAL_STORAGE
    LOCAL_DEV --> EMBEDDED
    
    VM_DEPLOY --> LOCAL_STORAGE
    VM_DEPLOY --> SELF_MANAGED
    
    K8S_DEPLOY --> S3_STORAGE
    K8S_DEPLOY --> MANAGED
    
    AWS_DEPLOY --> S3_STORAGE
    AWS_DEPLOY --> MANAGED
    
    AZURE_DEPLOY --> AZURE_STORAGE
    GCP_DEPLOY --> GCS_STORAGE
    
    MODAL_DEPLOY --> S3_STORAGE
    MODAL_DEPLOY --> MANAGED
    
    COGWIT --> S3_STORAGE
    COGWIT --> MANAGED
    
    style LOCAL_DEV fill:#a8e6cf
    style K8S_DEPLOY fill:#ffd3b6
    style COGWIT fill:#ffaaa5
    style MODAL_DEPLOY fill:#ff8b94
```

**Description:** Cognee supports multiple deployment scenarios from local development to cloud-native architectures, with flexible storage and database backends for different scale requirements.

---

## Summary

This architecture documentation provides comprehensive visualizations of the Cognee system:

- **High-Level**: Shows the overall system design and main components
- **Processing Flow**: Details the ECL pipeline and data transformations
- **Infrastructure**: Explains the multi-database architecture and provider integrations
- **Modules**: Breaks down the codebase organization and dependencies
- **Operations**: Illustrates each major operation (add, cognify, memify, search)
- **Deployment**: Covers various deployment options and configurations

The diagrams use consistent color coding:
- 🟢 Green (`#a8e6cf`) - Starting points and main components
- 🟠 Orange (`#ffd3b6`) - Processing and transformation steps
- 🔴 Red (`#ffaaa5`) - Advanced features and specialized components
- 🟥 Dark Red (`#ff8b94`) - End points and results

For more information, see:
- [README.md](README.md) - Project overview and quick start
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [Documentation](https://docs.cognee.ai) - Comprehensive online docs
