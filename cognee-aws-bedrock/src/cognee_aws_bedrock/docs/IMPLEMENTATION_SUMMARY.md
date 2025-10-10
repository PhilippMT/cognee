# AWS Bedrock Implementation Summary

## Overview

This document summarizes the implementation of AWS Bedrock foundation models support in Cognee, enabling access to Claude, Llama, Titan, and Nova models through AWS Bedrock's managed API.

## Implementation Details

### 1. Core Components Added

#### BedrockAdapter (`bedrock/adapter.py`)
- Implements `LLMInterface` for AWS Bedrock models
- Supports structured output generation via litellm with instructor
- Handles AWS authentication and region configuration
- Implements fallback model support for content policy violations
- Uses JSON mode for instructor compatibility with Bedrock models

**Key Features:**
- Automatic `bedrock/` prefix handling for model IDs
- AWS credentials support (explicit or default chain)
- Cross-region inference support via inference profiles
- Rate limiting and retry logic via decorators
- Content policy error handling with fallback models

#### LLMProvider Enum Extension (`get_llm_client.py`)
- Added `AWS_BEDROCK = "aws_bedrock"` to `LLMProvider` enum
- Added Bedrock adapter initialization in `get_llm_client()` function
- Maps LLMConfig fields to BedrockAdapter parameters

**Credential Mapping:**
- `aws_region_name` or `llm_endpoint` → region name
- `aws_access_key_id` or `llm_api_key` → AWS access key
- `aws_secret_access_key` or `llm_api_version` → AWS secret key

#### LLMConfig Extensions (`config.py`)
- Added AWS-specific configuration fields:
  - `aws_region_name: Optional[str]` - AWS region (default: None)
  - `aws_access_key_id: Optional[str]` - AWS access key ID
  - `aws_secret_access_key: Optional[str]` - AWS secret access key
- Updated `to_dict()` method to include AWS fields
- Updated `model_post_init()` for BAML AWS Bedrock support

**BAML Integration:**
- Maps `aws_bedrock` provider to `aws-bedrock` for BAML
- Uses `region` field instead of `base_url` for BAML AWS Bedrock
- Automatically uses `aws_region_name` or `baml_llm_endpoint` for region

### 2. BAML Framework Support

#### Updated Files
- `baml_src/acreate_structured_output.baml` - Added `AWSBedrock` client definition
- `baml_client/inlinedbaml.py` - Updated with AWS Bedrock client

**BAML Client Definition:**
```baml
client<llm> AWSBedrock {
    provider aws-bedrock
    options {
        model client_registry.model
        region client_registry.base_url
    }
}
```

### 3. Documentation

#### README.md
Comprehensive usage guide covering:
- Quick start for litellm_instructor and BAML
- Cross-region inference configuration
- Authentication methods (explicit credentials, default chain)
- IAM permissions requirements
- Model access setup in AWS console
- Configuration options and environment variables
- Troubleshooting guide
- Performance and cost optimization tips

#### MODELS.md
Complete model catalog including:
- Anthropic Claude models (3.7, 3.5, 3 - Sonnet, Haiku)
- Meta Llama models (3.1, 3.2 - 1B to 405B)
- Amazon Titan models (Text, Embeddings, Image)
- Amazon Nova models (Micro, Lite, Pro, Canvas, Reel, Sonic)
- Cross-region inference profile IDs
- Regional availability for eu-central-1, eu-north-1, eu-west-1
- Model capabilities and release dates

#### IMPLEMENTATION_SUMMARY.md
This document - technical implementation overview.

### 4. Testing

#### Unit Tests (`tests/unit/infrastructure/test_aws_bedrock_config.py`)
- Configuration creation with defaults
- Configuration with explicit credentials
- Configuration serialization (to_dict)
- Cross-region inference profile support
- Fallback model configuration
- BAML framework configuration
- Backward compatibility with legacy fields

**All tests use mocking and don't require AWS credentials.**

## Architecture Decisions

### 1. Model ID Format
- **Decision**: Support both `bedrock/model-id` and `model-id` formats
- **Rationale**: Litellm requires `bedrock/` prefix, but allow flexibility for users
- **Implementation**: Adapter automatically adds prefix if missing

### 2. Credentials Handling
- **Decision**: Support both explicit credentials and AWS default credential chain
- **Rationale**: Flexibility for different deployment scenarios (local dev, EC2, Lambda)
- **Implementation**: Optional parameters, falls back to AWS SDK defaults

### 3. Region Configuration
- **Decision**: Multiple field options for region (`aws_region_name`, `llm_endpoint`)
- **Rationale**: Backward compatibility and flexibility
- **Implementation**: Prioritize `aws_region_name`, fallback to `llm_endpoint`, default to `eu-central-1`

### 4. BAML Provider Mapping
- **Decision**: Map `aws_bedrock` to `aws-bedrock` for BAML
- **Rationale**: BAML expects hyphenated provider names
- **Implementation**: Transform in `model_post_init()` before registry configuration

### 5. Fallback Support
- **Decision**: Support fallback models for content policy violations
- **Rationale**: Resilience against content filtering, allows trying different models
- **Implementation**: Catch content policy errors, retry with fallback model/region

## Supported Models by Region

### EU Regions (eu-central-1, eu-north-1, eu-west-1)

**Generally Available:**
- Claude 3.7 Sonnet (latest)
- Claude 3.5 Sonnet v2
- Claude 3.5 Sonnet v1
- Claude 3 Sonnet
- Claude 3 Haiku
- Llama 3.2 (1B, 3B, 11B Vision, 90B Vision)
- Llama 3.1 (8B, 70B, 405B)
- Amazon Titan Text (Premier, Express, Lite)
- Amazon Titan Embeddings (v1, v2)
- Amazon Nova (Micro, Lite, Pro, Canvas, Reel, Sonic)

**Cross-Region Inference Profiles:**
- `eu.anthropic.claude-3-7-sonnet-20250219-v1:0` - Routes across EU regions
- More profiles available, see MODELS.md

## Configuration Examples

### litellm_instructor Framework

**Environment Variables:**
```bash
export LLM_PROVIDER=aws_bedrock
export LLM_MODEL=bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0
export AWS_REGION_NAME=eu-central-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Python Code:**
```python
import cognee

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"
```

### BAML Framework

**Environment Variables:**
```bash
export STRUCTURED_OUTPUT_FRAMEWORK=baml
export BAML_LLM_PROVIDER=aws_bedrock
export BAML_LLM_MODEL=anthropic.claude-3-7-sonnet-20250219-v1:0
export BAML_LLM_ENDPOINT=eu-central-1
```

**Python Code:**
```python
import cognee

cognee.config.structured_output_framework = "baml"
cognee.config.baml_llm_provider = "aws_bedrock"
cognee.config.baml_llm_model = "anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.baml_llm_endpoint = "eu-central-1"
```

### Cross-Region Inference

**Python Code:**
```python
import cognee

cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
cognee.config.aws_region_name = "eu-central-1"
# Requests automatically routed across EU regions
```

## Integration Points

### 1. LLM Client Factory (`get_llm_client()`)
- Entry point for obtaining LLM adapter
- Creates `BedrockAdapter` when provider is `aws_bedrock`
- Passes configuration from `LLMConfig`

### 2. Configuration System (`LLMConfig`)
- Central configuration for all LLM providers
- Validates and stores AWS Bedrock settings
- Initializes BAML registry with AWS Bedrock client

### 3. BAML Registry
- Registers AWS Bedrock as available provider
- Configures model and region from config
- Used when `structured_output_framework="baml"`

### 4. Rate Limiting & Retry
- Decorators from `rate_limiter.py` applied to adapter methods
- Handles AWS Bedrock rate limits
- Exponential backoff for retries

## Dependencies

### Required
- `litellm` - Unified LLM API, includes AWS Bedrock support
- `instructor` - Structured output framework
- `pydantic` - Data validation and serialization
- `boto3` (via litellm) - AWS SDK for Python

### Optional
- `baml-py` - BAML framework for structured outputs
- AWS CLI - For credential configuration

## Future Enhancements

1. **Streaming Support**: Add streaming response support for long-form generation
2. **Model Catalog API**: Fetch available models dynamically from AWS Bedrock
3. **Cost Tracking**: Track token usage and estimated costs
4. **Performance Metrics**: Log latency and throughput metrics
5. **Cross-Region Auto-Selection**: Automatically choose optimal region based on load
6. **Provisioned Throughput**: Support for provisioned throughput pricing
7. **Fine-tuned Models**: Support for custom fine-tuned models
8. **Additional Providers**: Support for more Bedrock model providers (Cohere, AI21, etc.)

## Testing Requirements

To test AWS Bedrock integration in production:

1. **AWS Account Setup**:
   - Create AWS account or use existing
   - Configure AWS credentials
   - Enable model access in Bedrock console

2. **IAM Permissions**:
   - Create IAM role/user with Bedrock permissions
   - Add `bedrock:InvokeModel` permission
   - Optionally add cross-region inference permissions

3. **Model Access**:
   - Navigate to AWS Bedrock console
   - Request access to desired models
   - Wait for approval (usually instant for most models)

4. **Configuration**:
   - Set environment variables or configure programmatically
   - Verify credentials with AWS CLI: `aws bedrock list-foundation-models --region eu-central-1`

5. **Integration Test**:
   - Run Cognee pipeline with AWS Bedrock configuration
   - Verify structured output generation works
   - Check logs for successful API calls

## Rollout Plan

### Phase 1: Initial Release (Completed)
- [x] Core adapter implementation
- [x] Configuration support
- [x] BAML integration
- [x] Documentation
- [x] Unit tests

### Phase 2: Validation (In Progress)
- [ ] Integration testing with actual AWS credentials
- [ ] Performance benchmarking
- [ ] Cost analysis
- [ ] User feedback collection

### Phase 3: Production Ready
- [ ] Additional examples and tutorials
- [ ] CI/CD integration tests
- [ ] Monitoring and alerting setup
- [ ] Performance optimization

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [LiteLLM Bedrock Provider](https://docs.litellm.ai/docs/providers/bedrock)
- [BAML Documentation](https://docs.boundaryml.com/)
- [Cognee Documentation](https://docs.cognee.ai/)

## Changelog

### v1.0.0 (Initial Implementation)
- Added BedrockAdapter for litellm_instructor framework
- Added AWS Bedrock provider to LLMProvider enum
- Extended LLMConfig with AWS-specific fields
- Implemented BAML framework support
- Created comprehensive documentation (README.md, MODELS.md)
- Added unit tests for configuration
- Documented all supported models in EU regions
- Implemented cross-region inference support

## Contributors

- GitHub Copilot - Primary implementation
- PhilippMT - Repository maintainer

## License

Follows the same license as the Cognee project.
