class ResponseModel {
    @@dynamic
}

// OpenAI client with environment model selection
client<llm> OpenAI {
    provider openai
    options {
        model client_registry.model
        api_key client_registry.api_key
    }
}

// AWS Bedrock client with environment configuration
client<llm> AWSBedrock {
    provider aws-bedrock
    options {
        model client_registry.model
        region client_registry.base_url
    }
}

function AcreateStructuredOutput(
    text_input: string,
    system_prompt: string,
) -> ResponseModel {
    client OpenAI

    prompt #"
        {{ system_prompt }}
        {{ ctx.output_format }}
        {{ _.role('user') }}
        {{ text_input }}
    "#
}
