---
applyTo: '**'
---

# Coding Preferences

- Python 3.10-3.13 with type hints
- Async/await patterns throughout
- Pydantic for data validation
- Constants for repeated literals to avoid linting issues

# Project Architecture

- Python 3.10-3.13 project
- Uses async/await patterns throughout
- Pydantic for data validation
- Type hints required for all functions
- Modular adapter pattern for infrastructure integrations
- AWS Bedrock integration uses instructor[bedrock] for LLM, litellm for embeddings

# Solutions Repository

## AWS Bedrock Migration (2025-10-29)

### Problem
Migrate cognee-aws-bedrock from litellm-based implementation to native instructor[bedrock]

### Solution
1. Updated dependencies to use `instructor[bedrock]` instead of litellm for LLM operations
2. Replaced `instructor.from_litellm()` with `instructor.from_bedrock(boto3_client)`
3. Used `asyncio.to_thread()` to wrap synchronous Bedrock SDK calls (boto3 doesn't support async natively)
4. Kept litellm for embedding operations (still needed)
5. Removed litellm-specific parameters (aws_region_name in create call) and used boto3 session configuration instead
6. Updated message format to use OpenAI-compatible format with system/user roles
7. Created separate boto3 clients for primary and fallback models with proper credential handling

### Key Changes
- Model ID: Strip 'bedrock/' prefix as instructor handles it internally
- Async pattern: Use `asyncio.to_thread(_sync_function)` for non-blocking calls
- Client initialization: Use boto3 Session → bedrock-runtime client → instructor.from_bedrock()
- Messages: Standard OpenAI format `[{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]`
- Parameters: Use `modelId` (Bedrock-native) instead of `model` in create calls
