# AWS Bedrock Batching Analysis

This document analyzes batching opportunities for AWS Bedrock LLM and embedding models, providing recommendations for optimizing throughput and cost.

## Table of Contents

- [Overview](#overview)
- [LLM Batch Inference](#llm-batch-inference)
- [Embedding Batch Processing](#embedding-batch-processing)
- [Implementation Strategies](#implementation-strategies)
- [Performance Optimization](#performance-optimization)
- [Cost Analysis](#cost-analysis)

---

## Overview

AWS Bedrock provides two types of batching capabilities:

1. **LLM Batch Inference** - Asynchronous batch processing for large-scale text generation
2. **Embedding Batching** - Automatic request batching for embedding generation

### Benefits of Batching

- **Cost Reduction**: Up to 50% lower costs compared to on-demand inference
- **Higher Throughput**: Process thousands of requests efficiently
- **Resource Optimization**: Better utilization of model capacity
- **Simplified Scaling**: Handle large volumes without rate limiting concerns

---

## LLM Batch Inference

### Supported Models

AWS Bedrock Batch Inference supports **Anthropic Claude models only**:

- ✅ Claude 3.7 Sonnet
- ✅ Claude 3.5 Sonnet (v1 and v2)
- ✅ Claude 3 Sonnet
- ✅ Claude 3 Haiku

**Not Supported**:
- ❌ Llama models
- ❌ Mistral models
- ❌ Titan models
- ❌ Nova models
- ❌ Cohere models

### How It Works

1. **Prepare Input**: Create JSONL file with batch requests
2. **Upload to S3**: Store input data in S3 bucket
3. **Create Batch Job**: Submit job via AWS Bedrock API
4. **Process**: AWS processes requests asynchronously
5. **Retrieve Results**: Download output from S3

### Batch Job Specifications

| Specification | Value |
|---------------|-------|
| **Max Requests** | 100,000 per job |
| **Job Duration** | Up to 24 hours |
| **Input Format** | JSONL (JSON Lines) |
| **S3 Storage** | Required for input/output |
| **Pricing** | ~50% discount vs on-demand |

### Implementation Example

```python
import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client('bedrock', region_name='eu-central-1')

# Prepare batch input (JSONL format)
batch_requests = [
    {
        "recordId": "request-1",
        "modelInput": {
            "messages": [
                {"role": "user", "content": "Summarize this text: ..."}
            ]
        }
    },
    {
        "recordId": "request-2",
        "modelInput": {
            "messages": [
                {"role": "user", "content": "Translate to French: ..."}
            ]
        }
    }
    # ... up to 100,000 requests
]

# Write to JSONL file
with open('batch_input.jsonl', 'w') as f:
    for request in batch_requests:
        f.write(json.dumps(request) + '\n')

# Upload to S3
s3 = boto3.client('s3')
s3.upload_file('batch_input.jsonl', 'my-bucket', 'input/batch_input.jsonl')

# Create batch inference job
response = bedrock.create_model_invocation_job(
    jobName='claude-batch-job-001',
    modelId='anthropic.claude-3-7-sonnet-20250219-v1:0',
    inputDataConfig={
        's3InputDataConfig': {
            's3Uri': 's3://my-bucket/input/batch_input.jsonl'
        }
    },
    outputDataConfig={
        's3OutputDataConfig': {
            's3Uri': 's3://my-bucket/output/'
        }
    },
    roleArn='arn:aws:iam::123456789012:role/BedrockBatchRole'
)

job_arn = response['jobArn']
print(f"Batch job created: {job_arn}")

# Monitor job status
status_response = bedrock.get_model_invocation_job(jobIdentifier=job_arn)
print(f"Job status: {status_response['status']}")

# Once complete, download results from S3
# Output format: JSONL with recordId and modelOutput
```

### Input Format Details

**JSONL Structure:**
```json
{"recordId": "unique-id-1", "modelInput": {"messages": [{"role": "user", "content": "Your prompt here"}], "max_tokens": 1024, "temperature": 0.7}}
{"recordId": "unique-id-2", "modelInput": {"messages": [{"role": "user", "content": "Another prompt"}], "max_tokens": 2048}}
```

**Required Fields:**
- `recordId`: Unique identifier for request (string)
- `modelInput`: Model parameters
  - `messages`: Chat messages array
  - Optional: `max_tokens`, `temperature`, `top_p`, `top_k`, `stop_sequences`

### Output Format

**JSONL Structure:**
```json
{"recordId": "unique-id-1", "modelOutput": {"content": [{"type": "text", "text": "Generated response"}], "stop_reason": "end_turn"}}
{"recordId": "unique-id-2", "modelOutput": {"content": [{"type": "text", "text": "Another response"}], "stop_reason": "end_turn"}}
```

### IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:CreateModelInvocationJob",
        "bedrock:GetModelInvocationJob",
        "bedrock:ListModelInvocationJobs",
        "bedrock:StopModelInvocationJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket/*",
        "arn:aws:s3:::my-bucket"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/BedrockBatchRole"
    }
  ]
}
```

### Use Cases for Batch Inference

1. **Large-Scale Content Generation**
   - Generating product descriptions for e-commerce catalogs
   - Creating marketing copy for thousands of products
   - Batch summarization of documents

2. **Data Processing Pipelines**
   - ETL workflows with LLM transformation
   - Batch classification or categorization
   - Large-scale data enrichment

3. **Research and Analysis**
   - Processing research papers
   - Analyzing customer feedback at scale
   - Historical data analysis

4. **Cost-Optimized Workloads**
   - Non-time-sensitive applications
   - Scheduled batch processing
   - Development and testing with large datasets

---

## Embedding Batch Processing

### Supported Models

All AWS Bedrock embedding models support batch processing:

- ✅ Amazon Titan Embed Text v1
- ✅ Amazon Titan Embed Text v2
- ✅ Amazon Titan Embed Image v1
- ✅ Cohere Embed English v3
- ✅ Cohere Embed Multilingual v3

### How Embedding Batching Works

Unlike LLM batch inference, embedding batching happens **automatically** within the real-time API:

1. **Client-Side Batching**: Group multiple texts in a single API call
2. **Model-Side Processing**: Model processes texts in parallel
3. **Automatic Chunking**: litellm handles splitting large batches

### Batch Size Limits

| Model | Max Texts/Request | Max Tokens/Text | Total Context |
|-------|-------------------|-----------------|---------------|
| **Titan Embed v2** | Limited by tokens | 8,192 | 50,000 chars |
| **Titan Embed v1** | Limited by tokens | 8,192 | ~50,000 chars |
| **Cohere Embed v3** | 96 texts | ~512 tokens | ~49,152 tokens |

### Implementation Example

```python
from cognee_aws_bedrock import BedrockEmbeddingAdapter

# Initialize adapter
adapter = BedrockEmbeddingAdapter(
    model="amazon.titan-embed-text-v2:0",
    dimensions=1024,
    aws_region_name="eu-central-1"
)

# Batch embed multiple texts efficiently
texts = [
    "First document to embed",
    "Second document to embed",
    "Third document to embed",
    # ... up to optimal batch size
]

# Single API call processes all texts
embeddings = await adapter.embed_text(texts)

print(f"Generated {len(embeddings)} embeddings")
# Each embedding is a list of floats with length = dimensions
```

### Optimal Batch Sizes

**Titan Embed v2:**
```python
# Recommended: 10-50 texts per batch
# Balance between throughput and token limits
OPTIMAL_BATCH_SIZE = 25

texts = load_documents()
for i in range(0, len(texts), OPTIMAL_BATCH_SIZE):
    batch = texts[i:i + OPTIMAL_BATCH_SIZE]
    embeddings = await adapter.embed_text(batch)
    save_embeddings(embeddings)
```

**Cohere Embed v3:**
```python
# Recommended: 32-96 texts per batch
# Cohere optimizes for this range
OPTIMAL_BATCH_SIZE = 64

texts = load_documents()
for i in range(0, len(texts), OPTIMAL_BATCH_SIZE):
    batch = texts[i:i + OPTIMAL_BATCH_SIZE]
    embeddings = await adapter.embed_text(batch)
    save_embeddings(embeddings)
```

### Automatic Chunking

The BedrockEmbeddingAdapter handles oversized inputs automatically:

```python
# If a single text exceeds token limit, it's automatically chunked
large_text = "..." * 10000  # Very large text

# Adapter splits and pools embeddings automatically
embedding = await adapter.embed_text([large_text])

# Result is a single embedding (averaged from chunks)
```

### Parallel Processing

For maximum throughput, process multiple batches in parallel:

```python
import asyncio

async def process_batch(texts):
    adapter = BedrockEmbeddingAdapter(
        model="amazon.titan-embed-text-v2:0",
        dimensions=1024,
        aws_region_name="eu-central-1"
    )
    return await adapter.embed_text(texts)

# Split into batches
all_texts = load_large_dataset()
batch_size = 25
batches = [all_texts[i:i + batch_size] for i in range(0, len(all_texts), batch_size)]

# Process batches in parallel (respect rate limits)
max_parallel = 10  # Adjust based on rate limits
results = []

for i in range(0, len(batches), max_parallel):
    parallel_batches = batches[i:i + max_parallel]
    batch_results = await asyncio.gather(*[process_batch(b) for b in parallel_batches])
    results.extend(batch_results)

print(f"Processed {len(results)} batches")
```

---

## Implementation Strategies

### Strategy 1: Hybrid Approach

Use batch inference for background processing, real-time for user-facing:

```python
# User-facing: Real-time inference
async def handle_user_query(query):
    register_bedrock_adapters(llm_region="eu-central-1")
    cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    response = await cognee.search("SIMILARITY", query)
    return response

# Background: Batch processing
def process_historical_data():
    # Prepare batch job for historical analysis
    create_batch_job(
        input_data=historical_queries,
        model="anthropic.claude-3-7-sonnet-20250219-v1:0"
    )
```

### Strategy 2: Queue-Based Batching

Accumulate requests and batch them periodically:

```python
from collections import deque
import asyncio

class BatchQueue:
    def __init__(self, max_size=100, max_wait=60):
        self.queue = deque()
        self.max_size = max_size
        self.max_wait = max_wait
        self.last_flush = time.time()
    
    async def add_request(self, request):
        self.queue.append(request)
        
        if len(self.queue) >= self.max_size or \
           (time.time() - self.last_flush) >= self.max_wait:
            await self.flush()
    
    async def flush(self):
        if not self.queue:
            return
        
        batch = list(self.queue)
        self.queue.clear()
        self.last_flush = time.time()
        
        # Create batch job
        await create_batch_job(batch)
```

### Strategy 3: Embedding Pipeline

Optimize embedding generation with batching:

```python
class EmbeddingPipeline:
    def __init__(self, batch_size=25):
        self.adapter = BedrockEmbeddingAdapter(
            model="amazon.titan-embed-text-v2:0",
            dimensions=1024,
            aws_region_name="eu-central-1"
        )
        self.batch_size = batch_size
    
    async def process_documents(self, documents):
        """Process documents in optimized batches"""
        all_embeddings = []
        
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i + self.batch_size]
            texts = [doc.content for doc in batch]
            
            embeddings = await self.adapter.embed_text(texts)
            all_embeddings.extend(embeddings)
            
            # Rate limiting
            await asyncio.sleep(0.1)
        
        return all_embeddings
```

---

## Performance Optimization

### LLM Batch Optimization

1. **Job Sizing**
   - Optimal: 1,000-10,000 requests per job
   - Avoid: Very small jobs (<100 requests) - overhead dominates
   - Consider: Multiple jobs for >50,000 requests

2. **Model Selection**
   - Claude 3 Haiku: Fastest, lowest cost
   - Claude 3 Sonnet: Balanced performance
   - Claude 3.7 Sonnet: Best quality, slower

3. **Parallel Jobs**
   - Run multiple batch jobs concurrently
   - Monitor with `list_model_invocation_jobs()`
   - Max concurrent: Check service quotas

### Embedding Batch Optimization

1. **Batch Size**
   - Titan: 10-50 texts (token-dependent)
   - Cohere: 32-96 texts
   - Test optimal size for your use case

2. **Parallel Requests**
   - Max parallel: 5-10 concurrent requests
   - Respect rate limits: ~60 requests/minute
   - Use exponential backoff for errors

3. **Text Preprocessing**
   - Clean and normalize text before embedding
   - Remove very short texts (<10 tokens)
   - Handle special characters

4. **Caching**
   - Cache embeddings for repeated texts
   - Use deterministic IDs (hash of content)
   - Reduce redundant API calls

---

## Cost Analysis

### LLM Batch Inference Savings

| Model | On-Demand | Batch | Savings |
|-------|-----------|-------|---------|
| **Claude 3.7 Sonnet** | $0.003/1K input<br>$0.015/1K output | **~50% discount** | 50% |
| **Claude 3.5 Sonnet** | $0.003/1K input<br>$0.015/1K output | **~50% discount** | 50% |
| **Claude 3 Haiku** | $0.00025/1K input<br>$0.00125/1K output | **~50% discount** | 50% |

**Example Cost Calculation:**

Processing 1 million requests with Claude 3.7 Sonnet:
- Input: 500 tokens/request
- Output: 200 tokens/request

**On-Demand:**
- Input: (1M * 500) / 1000 * $0.003 = $1,500
- Output: (1M * 200) / 1000 * $0.015 = $3,000
- **Total: $4,500**

**Batch:**
- **Total: ~$2,250** (50% savings = **$2,250 saved**)

### Embedding Cost Comparison

Embedding costs are the same for batch and real-time, but batching improves:
- **Throughput**: Process more embeddings/second
- **Efficiency**: Reduce overhead and latency
- **Resource Usage**: Better utilize API rate limits

**Titan Embed v2 Pricing:**
- $0.00002 per 1,000 tokens

**Example:**
- 1 million documents @ 500 tokens each
- Cost: (1M * 500) / 1000 * $0.00002 = **$10**

---

## Best Practices

### For LLM Batch Inference

1. ✅ Use for non-time-sensitive workloads
2. ✅ Batch similar requests together
3. ✅ Monitor job status regularly
4. ✅ Implement error handling and retries
5. ✅ Use S3 lifecycle policies for cleanup
6. ✅ Test with small batches first

### For Embedding Batching

1. ✅ Group similar-length texts
2. ✅ Implement caching for repeated texts
3. ✅ Use parallel processing with rate limiting
4. ✅ Monitor token usage per request
5. ✅ Handle context window errors gracefully
6. ✅ Preprocess and normalize text

### Common Pitfalls

❌ **Avoid:**
- Very small batch jobs (<100 requests)
- Exceeding 100,000 requests per job
- Not monitoring job status
- Forgetting IAM permissions for S3
- Ignoring rate limits for embeddings
- Not implementing retry logic

---

## Monitoring and Metrics

### Key Metrics to Track

1. **Batch Job Metrics**
   - Job completion time
   - Success rate
   - Failed requests
   - Cost per job

2. **Embedding Metrics**
   - Requests per minute
   - Tokens per request
   - Error rate
   - Latency

3. **Cost Metrics**
   - Total token usage
   - Cost per 1K tokens
   - Savings from batching

### Monitoring Implementation

```python
import time
from dataclasses import dataclass

@dataclass
class BatchMetrics:
    job_id: str
    start_time: float
    end_time: float = None
    requests_count: int = 0
    success_count: int = 0
    error_count: int = 0
    total_tokens: int = 0
    
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def success_rate(self):
        if self.requests_count == 0:
            return 0
        return self.success_count / self.requests_count

# Usage
metrics = BatchMetrics(
    job_id="batch-001",
    start_time=time.time(),
    requests_count=1000
)

# ... process batch ...

metrics.end_time = time.time()
metrics.success_count = 980
metrics.error_count = 20
metrics.total_tokens = 500000

print(f"Duration: {metrics.duration():.2f}s")
print(f"Success rate: {metrics.success_rate():.2%}")
```

---

## Conclusion

AWS Bedrock batching provides significant opportunities for cost optimization and performance improvement:

- **LLM Batch Inference**: 50% cost savings for large-scale text generation
- **Embedding Batching**: Improved throughput with automatic batching
- **Hybrid Strategies**: Combine batch and real-time for optimal results

**Recommendations:**

1. Use batch inference for **Claude models** in non-time-sensitive scenarios
2. Implement **intelligent batching** for embeddings with 25-64 texts per batch
3. Monitor metrics and optimize based on your specific use case
4. Start small, measure, and scale gradually

---

Last Updated: January 2025
