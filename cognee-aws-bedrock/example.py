"""
Example usage of AWS Bedrock adapter with Cognee
"""

import asyncio
from cognee_aws_bedrock import register_bedrock_adapters


async def main():
    # Register AWS Bedrock adapters with custom configuration
    register_bedrock_adapters(
        llm_region="eu-west-1",
        llm_profile="my-llm-profile",
        embedding_region="eu-central-1",
        embedding_profile="my-embedding-profile"
    )
    
    # Import cognee after registration
    import cognee
    
    # Configure LLM
    cognee.config.llm_provider = "aws_bedrock"
    cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    # Configure Embeddings
    cognee.config.embedding_provider = "bedrock"
    cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
    cognee.config.embedding_dimensions = 1024
    
    # Use Cognee as normal
    text = """
    AWS Bedrock provides access to foundation models from leading AI companies.
    It supports models from Anthropic, Meta, Amazon, and Cohere.
    """
    
    await cognee.add(text)
    await cognee.cognify()
    
    # Search the knowledge graph
    results = await cognee.search("SIMILARITY", "What is AWS Bedrock?")
    print("Search results:", results)


if __name__ == "__main__":
    asyncio.run(main())
