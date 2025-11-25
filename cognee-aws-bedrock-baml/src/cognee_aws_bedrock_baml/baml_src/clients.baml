// BAML Configuration for AWS Bedrock Foundation Models
// This file defines LLM clients for AWS Bedrock using the aws-bedrock provider

// ============================================================================
// Anthropic Claude Models - Full tools support
// ============================================================================

// Claude 3.5 Sonnet v2 - Latest generation, best performance
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

// Claude 3.5 Sonnet v1 - Production workloads
client<llm> ClaudeSonnet35V1 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-sonnet-20240620-v1:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// Claude 3.5 Haiku - Fast and cost-effective
client<llm> ClaudeHaiku35 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-5-haiku-20241022-v1:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// Claude 3 Sonnet - Established workloads
client<llm> ClaudeSonnet3 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-sonnet-20240229-v1:0"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}

// Claude 3 Haiku - Ultra-fast responses
client<llm> ClaudeHaiku3 {
  provider aws-bedrock
  options {
    model "anthropic.claude-3-haiku-20240307-v1:0"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}

// ============================================================================
// Amazon Nova Models - Multimodal capabilities
// ============================================================================

// Amazon Nova Pro - Multimodal (text, image, video)
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

// Amazon Nova Lite - Cost-effective multimodal
client<llm> NovaLite {
  provider aws-bedrock
  options {
    model "amazon.nova-lite-v1:0"
    inference_configuration {
      max_tokens 5120
      temperature 0.7
    }
  }
}

// Amazon Nova Micro - Text-only, extremely cost-effective
client<llm> NovaMicro {
  provider aws-bedrock
  options {
    model "amazon.nova-micro-v1:0"
    inference_configuration {
      max_tokens 5120
      temperature 0.7
    }
  }
}

// ============================================================================
// Meta Llama Models - Open source
// ============================================================================

// Llama 3.3 70B Instruct - Latest open-source
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

// Llama 3.2 90B Vision Instruct
client<llm> Llama32_90B_Vision {
  provider aws-bedrock
  options {
    model "meta.llama3-2-90b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.2 11B Vision Instruct
client<llm> Llama32_11B_Vision {
  provider aws-bedrock
  options {
    model "meta.llama3-2-11b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.2 3B Instruct - Edge deployment
client<llm> Llama32_3B {
  provider aws-bedrock
  options {
    model "meta.llama3-2-3b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.2 1B Instruct - Ultra-efficient
client<llm> Llama32_1B {
  provider aws-bedrock
  options {
    model "meta.llama3-2-1b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.1 405B Instruct - Largest
client<llm> Llama31_405B {
  provider aws-bedrock
  options {
    model "meta.llama3-1-405b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.1 70B Instruct
client<llm> Llama31_70B {
  provider aws-bedrock
  options {
    model "meta.llama3-1-70b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// Llama 3.1 8B Instruct - Efficient
client<llm> Llama31_8B {
  provider aws-bedrock
  options {
    model "meta.llama3-1-8b-instruct-v1:0"
    inference_configuration {
      max_tokens 2048
      temperature 0.7
    }
  }
}

// ============================================================================
// Mistral AI Models - European compliance
// ============================================================================

// Mistral Large 2 (2407) - Latest
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

// Mistral Large (2402)
client<llm> MistralLarge {
  provider aws-bedrock
  options {
    model "mistral.mistral-large-2402-v1:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// Mistral Small (2402)
client<llm> MistralSmall {
  provider aws-bedrock
  options {
    model "mistral.mistral-small-2402-v1:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// Mixtral 8x7B Instruct - Mixture of experts
client<llm> Mixtral8x7B {
  provider aws-bedrock
  options {
    model "mistral.mixtral-8x7b-instruct-v0:1"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}

// ============================================================================
// Amazon Titan Models - AWS-native (JSON mode only)
// ============================================================================

// Titan Text Premier
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

// Titan Text Express
client<llm> TitanExpress {
  provider aws-bedrock
  options {
    model "amazon.titan-text-express-v1"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// Titan Text Lite
client<llm> TitanLite {
  provider aws-bedrock
  options {
    model "amazon.titan-text-lite-v1"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}

// ============================================================================
// Cohere Models - RAG and search optimized
// ============================================================================

// Command R+ - Best for RAG
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

// Command R - Cost-effective RAG
client<llm> CommandR {
  provider aws-bedrock
  options {
    model "cohere.command-r-v1:0"
    inference_configuration {
      max_tokens 4096
      temperature 0.7
    }
  }
}

// ============================================================================
// Cross-Region Inference Profiles (EU)
// ============================================================================

// EU Cross-region Claude 3.5 Sonnet v2
client<llm> EUClaudeSonnet35V2 {
  provider aws-bedrock
  options {
    model "eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
    inference_configuration {
      max_tokens 8192
      temperature 0.7
    }
  }
}

// EU Cross-region Amazon Nova Pro
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

// EU Cross-region Cohere Command R+
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
