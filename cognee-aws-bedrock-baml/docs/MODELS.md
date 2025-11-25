# AWS Bedrock Foundation Models - BAML Configuration Guide

This document provides comprehensive configuration information for all AWS Bedrock foundation models available in **eu-central-1** and **eu-north-1** regions, with proper setup for BAML's `aws-bedrock` provider.

## Table of Contents

- [Quick Reference](#quick-reference)
- [BAML Client Configuration](#baml-client-configuration)
- [Anthropic Claude Models](#anthropic-claude-models)
- [Amazon Nova Models](#amazon-nova-models)
- [Meta Llama Models](#meta-llama-models)
- [Mistral AI Models](#mistral-ai-models)
- [Amazon Titan Models](#amazon-titan-models)
- [Cohere Models](#cohere-models)
- [Cross-Region Inference Profiles](#cross-region-inference-profiles)

## Quick Reference

### Models with Tools Support (BAML tools mode)

All models below support structured outputs through BAML's `aws-bedrock` provider:

| Provider | Model Count | Best For |
|----------|-------------|----------|
| Anthropic Claude | 5 models | Complex reasoning, multimodal understanding |
| Amazon Nova | 3 models | Multimodal (text, image, video), cost-effective |
| Meta Llama | 8 models | Open-source, customizable, various sizes |
| Mistral AI | 4 models | European compliance, strong performance |
| Cohere | 2 models | RAG, search, multilingual |

### Models without Tools Support (JSON mode only)

- **Amazon Titan** models (3 models): Use JSON mode

---

## BAML Client Configuration

### Basic Client Definition

```baml
client<llm> MyBedrockClient {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### With AWS Credentials

```baml
client<llm> MyBedrockClient {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    region "eu-central-1"
    access_key_id env.AWS_ACCESS_KEY_ID
    secret_access_key env.AWS_SECRET_ACCESS_KEY
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### With AWS Profile

```baml
client<llm> MyBedrockClient {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    profile "my-aws-profile"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

---

## Anthropic Claude Models

All Claude models support tools/function calling with BAML.

### Claude 3.5 Sonnet v2 (Latest)

**Model ID:** `anthropic.claude-3-5-sonnet-20241022-v2:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes
- **Best For:** Most complex tasks, latest features, best reasoning

**BAML Configuration:**
```baml
client<llm> ClaudeSonnet35V2 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### Claude 3.5 Haiku

**Model ID:** `anthropic.claude-3-5-haiku-20241022-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 200,000 tokens
- **Max Output:** 8,192 tokens
- **Input Modalities:** Text, Image
- **Tools Support:** ✅ Yes
- **Best For:** Fast responses, cost-effective, high volume

---

## Amazon Nova Models

Amazon's newest multimodal models with tools support.

### Nova Pro

**Model ID:** `amazon.nova-pro-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 300,000 tokens
- **Max Output:** 5,120 tokens
- **Input Modalities:** Text, Image, Video
- **Tools Support:** ✅ Yes
- **Best For:** Multimodal understanding, video analysis, complex tasks

**BAML Configuration:**
```baml
client<llm> NovaPro {
  provider aws-bedrock
  options {
    model "amazon.nova-pro-v1:0"
    inference_configuration {
      max_tokens 5120
      temperature 0.7
    }
  }
}
```

### Nova Lite / Nova Micro

**Model IDs:**
- `amazon.nova-lite-v1:0` - Cost-effective multimodal
- `amazon.nova-micro-v1:0` - Text-only, extremely cost-effective

---

## Meta Llama Models

Open-source models with tools support.

### Llama 3.3 70B Instruct

**Model ID:** `meta.llama3-3-70b-instruct-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 2,048 tokens
- **Input Modalities:** Text
- **Tools Support:** ✅ Yes
- **Best For:** Latest Llama, strong performance, open-source

**BAML Configuration:**
```baml
client<llm> Llama33_70B {
  provider aws-bedrock
  options {
    model "meta.llama3-3-70b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}
```

### Additional Llama Models

| Model ID | Size | Vision |
|----------|------|--------|
| `meta.llama3-2-90b-instruct-v1:0` | 90B | ✅ Yes |
| `meta.llama3-2-11b-instruct-v1:0` | 11B | ✅ Yes |
| `meta.llama3-2-3b-instruct-v1:0` | 3B | ❌ No |
| `meta.llama3-2-1b-instruct-v1:0` | 1B | ❌ No |
| `meta.llama3-1-405b-instruct-v1:0` | 405B | ❌ No |
| `meta.llama3-1-70b-instruct-v1:0` | 70B | ❌ No |
| `meta.llama3-1-8b-instruct-v1:0` | 8B | ❌ No |

---

## Mistral AI Models

European AI company models with tools support.

### Mistral Large 2 (2407)

**Model ID:** `mistral.mistral-large-2407-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 8,192 tokens
- **Tools Support:** ✅ Yes
- **Best For:** Latest Mistral, best performance, complex reasoning

**BAML Configuration:**
```baml
client<llm> MistralLarge2 {
  provider aws-bedrock
  options {
    model "mistral.mistral-large-2407-v1:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

### Additional Mistral Models

| Model ID | Context |
|----------|---------|
| `mistral.mistral-large-2402-v1:0` | 32K |
| `mistral.mistral-small-2402-v1:0` | 32K |
| `mistral.mixtral-8x7b-instruct-v0:1` | 32K |

---

## Amazon Titan Models

**Note:** Titan models do NOT support tools. Use JSON mode.

### Titan Text Premier

**Model ID:** `amazon.titan-text-premier-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 32,000 tokens
- **Max Output:** 3,072 tokens
- **Tools Support:** ❌ No (JSON mode)
- **Best For:** RAG, summarization, AWS-native

**BAML Configuration:**
```baml
client<llm> TitanPremier {
  provider aws-bedrock
  options {
    model "amazon.titan-text-premier-v1:0"
    inference_configuration {
      max_tokens 3072
      temperature 0.7
    }
  }
}
```

---

## Cohere Models

Command R series with tools support.

### Command R+

**Model ID:** `cohere.command-r-plus-v1:0`

- **Regions:** eu-central-1, eu-north-1
- **Context Window:** 128,000 tokens
- **Max Output:** 4,096 tokens
- **Tools Support:** ✅ Yes
- **Best For:** RAG, search, retrieval, complex reasoning

**BAML Configuration:**
```baml
client<llm> CommandRPlus {
  provider aws-bedrock
  options {
    model "cohere.command-r-plus-v1:0"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}
```

---

## Cross-Region Inference Profiles

For automatic load distribution across EU regions, use cross-region inference profiles with the `eu.` prefix:

**Available Cross-Region Profiles:**

```baml
// Claude with cross-region
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

// Nova with cross-region
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

// Cohere with cross-region
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

---

## Best Practices

1. **Start with Claude 3.5 Sonnet v2** for best overall performance
2. **Use cross-region profiles** (`eu.*`) for automatic load distribution
3. **Match model to task**: Don't use 405B for simple tasks
4. **Consider cost**: Haiku/Nova Micro for high-volume simple tasks
5. **Test multiple models**: Use different models for different components
6. **Monitor usage**: Set up CloudWatch alarms for cost tracking

---

## References

- [BAML Documentation](https://docs.boundaryml.com/)
- [BAML AWS Bedrock Provider](https://docs.boundaryml.com/ref/llm-client-providers/aws-bedrock)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
