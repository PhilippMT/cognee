# Cross-Region Inference Profiles

Cross-region inference profiles allow routing requests across multiple AWS regions for improved availability and latency.

**Last Updated: December 2025**

## Available Cross-Region Profiles

### Claude Models

| Profile ID | Base Model |
|------------|------------|
| `eu.anthropic.claude-sonnet-4-5-20250929-v1:0` | Claude Sonnet 4.5 |
| `eu.anthropic.claude-sonnet-4-20250514-v1:0` | Claude Sonnet 4 |
| `eu.anthropic.claude-opus-4-5-20251101-v1:0` | Claude Opus 4.5 |
| `eu.anthropic.claude-haiku-4-5-20251001-v1:0` | Claude Haiku 4.5 |
| `eu.anthropic.claude-3-7-sonnet-20250219-v1:0` | Claude 3.7 Sonnet |
| `eu.anthropic.claude-3-5-haiku-20241022-v1:0` | Claude 3.5 Haiku |
| `eu.anthropic.claude-3-haiku-20240307-v1:0` | Claude 3 Haiku |

### Amazon Nova Models

| Profile ID | Base Model |
|------------|------------|
| `eu.amazon.nova-2-lite-v1:0` | Nova 2 Lite |
| `eu.amazon.nova-pro-v1:0` | Nova Pro |
| `eu.amazon.nova-lite-v1:0` | Nova Lite |
| `eu.amazon.nova-micro-v1:0` | Nova Micro |

### Meta Llama Models

| Profile ID | Base Model |
|------------|------------|
| `eu.meta.llama3-2-3b-instruct-v1:0` | Llama 3.2 3B |
| `eu.meta.llama3-2-1b-instruct-v1:0` | Llama 3.2 1B |

### Mistral Models

| Profile ID | Base Model |
|------------|------------|
| `eu.mistral.pixtral-large-2502-v1:0` | Pixtral Large |

### Cohere Embeddings

| Profile ID | Base Model |
|------------|------------|
| `eu.cohere.embed-v4:0` | Embed v4 |

### TwelveLabs Models

| Profile ID | Base Model |
|------------|------------|
| `eu.twelvelabs.pegasus-1-2-v1:0` | Pegasus v1.2 |
| `eu.twelvelabs.marengo-embed-2-7-v1:0` | Marengo Embed v2.7 |

## Usage Example

```python
from cognee_aws_bedrock_baml import BamlBedrockLLMAdapter

# Use cross-region profile for better availability
adapter = BamlBedrockLLMAdapter(
    model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="eu-central-1"
)
```

## Benefits

1. **Higher Availability**: Requests can be routed to multiple regions
2. **Lower Latency**: AWS routes to the nearest available region
3. **Automatic Failover**: If one region is unavailable, requests go to another
4. **Same API**: Use the same model ID with `eu.` prefix
