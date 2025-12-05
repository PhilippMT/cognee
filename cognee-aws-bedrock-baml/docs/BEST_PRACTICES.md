# Best Practices

Recommendations for using AWS Bedrock with BAML in production.

## Model Selection

### 1. Start with Claude 3.5 Sonnet v2

For most use cases, Claude 3.5 Sonnet v2 provides the best balance of:
- Reasoning capability
- Response quality
- Cost efficiency

```python
cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
```

### 2. Match Model to Task

| Task | Recommended Model |
|------|-------------------|
| Complex reasoning | Claude 3.5 Sonnet v2 |
| Simple/fast tasks | Claude 3.5 Haiku |
| Very long documents | Jamba 1.5 Large (256K) |
| Multimodal (image/video) | Nova Pro |
| Open source requirement | Llama 3.3 70B |
| European compliance | Mistral Large 2 |
| RAG/Search | Command R+ |

### 3. Cost Optimization

| Priority | Model |
|----------|-------|
| Lowest cost | Nova Micro, Haiku |
| Balanced | Claude 3.5 Haiku |
| Best performance | Claude 3.5 Sonnet v2 |

## Region Strategy

### 1. Use Cross-Region Profiles

For production workloads, use cross-region profiles for resilience:

```python
cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

### 2. Regional Considerations

| Region | Pros | Cons |
|--------|------|------|
| eu-central-1 | Most models, GDPR | Higher latency for Nordic |
| eu-west-1 | All models, good connectivity | - |
| eu-north-1 | Nordic compliance | Some models limited |

## Embedding Selection

### 1. Default Choice

For most use cases:
```python
cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
cognee.config.embedding_dimensions = 1024
```

### 2. Multilingual Content

For non-English or mixed content:
```python
cognee.config.embedding_model = "bedrock/cohere.embed-multilingual-v3"
```

### 3. Dimension Trade-offs

| Dimension | Storage | Accuracy | Speed |
|-----------|---------|----------|-------|
| 256 | Lowest | Lower | Fastest |
| 512 | Medium | Good | Fast |
| 1024 | Higher | Best | Normal |

## Error Handling

### 1. Implement Fallbacks

```python
from cognee_aws_bedrock_baml import BamlBedrockLLMAdapter

adapter = BamlBedrockLLMAdapter(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_completion_tokens=4096,
    aws_region_name="eu-central-1",
    fallback_model="anthropic.claude-3-5-haiku-20241022-v1:0",
    fallback_aws_region_name="eu-west-1"
)
```

### 2. Handle Rate Limits

The adapter includes automatic retry with exponential backoff.

## Monitoring

### 1. CloudWatch Metrics

Monitor these key metrics:
- `InvocationLatency`
- `InvocationCount`
- `ThrottledCount`
- `ModelLatency`

### 2. Cost Tracking

Set up AWS Cost Explorer budgets for Bedrock usage.

## Security

### 1. Use IAM Roles

Prefer IAM roles over access keys:
```python
# Uses default credential chain (IAM role, env vars, etc.)
adapter = BamlBedrockLLMAdapter(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_completion_tokens=4096,
    aws_region_name="eu-central-1"
)
```

### 2. Least Privilege

Minimum IAM permissions needed:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*:*:foundation-model/*"
    }
  ]
}
```

## Performance Optimization

### 1. Token Limits

Set appropriate `max_tokens` for your use case:
- Short responses: 512-1024
- Medium responses: 2048-4096
- Long content: 8192+

### 2. Temperature Settings

| Use Case | Temperature |
|----------|-------------|
| Factual/deterministic | 0.0-0.3 |
| Balanced | 0.5-0.7 |
| Creative | 0.8-1.0 |

### 3. Batch Processing

For high volume, consider:
- Using smaller models for simple tasks
- Implementing request queuing
- Using provisioned throughput

## Testing

### 1. Test Multiple Models

Always test with different models to find the best fit:
```python
models_to_test = [
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    "meta.llama3-3-70b-instruct-v1:0"
]
```

### 2. Validate Outputs

Test structured output parsing with your Pydantic models.

## References

- [AWS Bedrock Best Practices](https://docs.aws.amazon.com/bedrock/latest/userguide/best-practices.html)
- [BAML Documentation](https://docs.boundaryml.com/)
- [AWS Well-Architected ML Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/)
