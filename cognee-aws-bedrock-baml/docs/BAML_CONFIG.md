# BAML Client Configuration

This document explains how to configure BAML clients for AWS Bedrock.

## Basic Client Definition

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

## With AWS Credentials

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

## With AWS Profile

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

## Inference Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `max_tokens` | int | Maximum tokens in response |
| `temperature` | float | Randomness (0.0-1.0) |
| `top_p` | float | Nucleus sampling |
| `stop_sequences` | list | Stop generation tokens |

## Example: Claude 3.5 Sonnet

```baml
client<llm> ClaudeSonnet35V2 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20241022-v2:0"
    region "eu-central-1"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}
```

## Example: Nova Pro (Multimodal)

```baml
client<llm> NovaPro {
  provider aws-bedrock
  options {
    model "amazon.nova-pro-v1:0"
    region "eu-west-1"
    inference_configuration {
      max_tokens 5120
      temperature 0.7
    }
  }
}
```

## Example: Llama 3.3 70B

```baml
client<llm> Llama33_70B {
  provider aws-bedrock
  options {
    model "meta.llama3-3-70b-instruct-v1:0"
    region "eu-north-1"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}
```

## Example: Jamba 1.5 Large (256K context)

```baml
client<llm> Jamba15Large {
  provider aws-bedrock
  options {
    model "ai21.jamba-1-5-large-v1:0"
    region "eu-central-1"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}
```

## Python Adapter Usage

```python
from cognee_aws_bedrock_baml import BamlBedrockLLMAdapter

adapter = BamlBedrockLLMAdapter(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_completion_tokens=4096,
    aws_region_name="eu-central-1",
    aws_profile_name="my-profile"  # Optional
)
```

## Environment Variables

```bash
export AWS_REGION=eu-central-1
export AWS_PROFILE=my-profile
# Or use explicit credentials:
export AWS_ACCESS_KEY_ID=your-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-key
```
