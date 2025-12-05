# Cross-Region Inference Profiles

AWS Bedrock supports cross-region inference profiles for automatic load distribution.

## What are Cross-Region Profiles?

Cross-region inference profiles allow you to:
- Automatically distribute load across multiple regions
- Improve availability and resilience
- Use a single endpoint that routes to available regions

## EU Cross-Region Prefix

Use the `eu.` prefix to enable cross-region inference:

```
eu.<provider>.<model-id>
```

## Available EU Cross-Region Profiles

### Anthropic Claude

| Cross-Region Profile | Base Model |
|---------------------|------------|
| `eu.anthropic.claude-3-5-sonnet-20241022-v2:0` | Claude 3.5 Sonnet v2 |
| `eu.anthropic.claude-3-5-sonnet-20240620-v1:0` | Claude 3.5 Sonnet v1 |
| `eu.anthropic.claude-3-5-haiku-20241022-v1:0` | Claude 3.5 Haiku |
| `eu.anthropic.claude-3-sonnet-20240229-v1:0` | Claude 3 Sonnet |
| `eu.anthropic.claude-3-haiku-20240307-v1:0` | Claude 3 Haiku |

### Amazon Nova

| Cross-Region Profile | Base Model |
|---------------------|------------|
| `eu.amazon.nova-pro-v1:0` | Nova Pro |
| `eu.amazon.nova-lite-v1:0` | Nova Lite |
| `eu.amazon.nova-micro-v1:0` | Nova Micro |

### Cohere

| Cross-Region Profile | Base Model |
|---------------------|------------|
| `eu.cohere.command-r-plus-v1:0` | Command R+ |
| `eu.cohere.command-r-v1:0` | Command R |

## BAML Configuration Examples

### Claude with Cross-Region

```baml
client<llm> EUClaudeSonnet {
  provider aws-bedrock
  options {
    model "eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### Nova with Cross-Region

```baml
client<llm> EUNovaPro {
  provider aws-bedrock
  options {
    model "eu.amazon.nova-pro-v1:0"
    inference_configuration {
      max_tokens 5120
      temperature 0.7
    }
  }
}
```

### Cohere with Cross-Region

```baml
client<llm> EUCommandRPlus {
  provider aws-bedrock
  options {
    model "eu.cohere.command-r-plus-v1:0"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}
```

## Python Usage

```python
import cognee

# Using cross-region profile
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

## Benefits

1. **High Availability**: Automatic failover if one region is unavailable
2. **Load Distribution**: Requests are distributed across regions
3. **Reduced Latency**: Routes to nearest available region
4. **Simple Configuration**: Single model ID for multiple regions

## Limitations

- Not all models have cross-region profiles
- Some newer models may only be in specific regions
- Pricing may vary by region

## When to Use

✅ **Use cross-region profiles when:**
- You need high availability
- Your users are across Europe
- You want automatic load balancing

❌ **Use specific regions when:**
- You need data residency compliance
- You want predictable latency
- You need specific regional features
