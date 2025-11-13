"""
Example usage of AWS Bedrock adapter with Cognee using instructor[bedrock]

This example demonstrates:
1. Using the new instructor[bedrock] implementation
2. Tools/function calling support with BEDROCK_TOOLS mode
3. Multiple model configurations
4. Cross-region inference profiles
"""

import asyncio
from cognee_aws_bedrock import register_bedrock_adapters


async def main():
    print("=" * 80)
    print("AWS Bedrock with instructor[bedrock] - Example Usage")
    print("=" * 80)

    # Register AWS Bedrock adapters with custom configuration
    print("\n1. Registering Bedrock adapters...")
    register_bedrock_adapters(
        llm_region="eu-central-1",
        llm_profile="default",  # Optional: use your AWS profile
        embedding_region="eu-central-1",
        embedding_profile="default",
    )

    # Import cognee after registration
    import cognee

    # Example 1: Using Claude 3.5 Sonnet v2 (latest) with tools support
    print("\n2. Configuring LLM - Claude 3.5 Sonnet v2 (BEDROCK_TOOLS mode)")
    cognee.config.llm_provider = "aws_bedrock"
    cognee.config.llm_model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
    cognee.config.aws_region_name = "eu-central-1"

    # Configure Embeddings
    print("3. Configuring Embeddings - Titan Embed Text v2")
    cognee.config.embedding_provider = "bedrock"
    cognee.config.embedding_model = "bedrock/amazon.titan-embed-text-v2:0"
    cognee.config.embedding_dimensions = 1024

    # Use Cognee with sample data
    print("\n4. Adding and processing data...")
    text = """
    AWS Bedrock provides access to foundation models from leading AI companies.
    It supports models from Anthropic (Claude 3.5 Sonnet), Meta (Llama 3.x), 
    Amazon (Nova and Titan), Mistral AI, and Cohere.
    
    The new instructor[bedrock] integration provides native tools/function calling 
    support for better structured outputs with BEDROCK_TOOLS mode.
    """

    await cognee.add(text, dataset_name="bedrock_demo")
    print("   ✓ Data added successfully")

    await cognee.cognify(["bedrock_demo"])
    print("   ✓ Data processed with cognify pipeline")

    # Search the knowledge graph
    print("\n5. Searching knowledge graph...")
    results = await cognee.search("SIMILARITY", "What models does AWS Bedrock support?")
    print(f"   ✓ Found {len(results)} results")
    if results:
        print(f"\n   First result: {str(results[0])[:200]}...")

    # Example 2: Using Amazon Nova Pro for multimodal tasks
    print("\n" + "=" * 80)
    print("Example 2: Amazon Nova Pro (Multimodal)")
    print("=" * 80)
    cognee.config.llm_model = "bedrock/amazon.nova-pro-v1:0"
    print("   ✓ Switched to Amazon Nova Pro (supports text, image, video)")

    # Example 3: Using cross-region inference profile
    print("\n" + "=" * 80)
    print("Example 3: Cross-Region Inference Profile")
    print("=" * 80)
    cognee.config.llm_model = "bedrock/eu.anthropic.claude-3-5-sonnet-20241022-v2:0"
    print("   ✓ Using EU cross-region profile for automatic load distribution")

    # Example 4: Using Meta Llama (open-source)
    print("\n" + "=" * 80)
    print("Example 4: Meta Llama 3.3 70B (Open Source)")
    print("=" * 80)
    cognee.config.llm_model = "bedrock/meta.llama3-3-70b-instruct-v1:0"
    print("   ✓ Switched to Llama 3.3 70B (latest open-source model)")

    # Example 5: Using Mistral for European compliance
    print("\n" + "=" * 80)
    print("Example 5: Mistral Large 2 (European AI)")
    print("=" * 80)
    cognee.config.llm_model = "bedrock/mistral.mistral-large-2407-v1:0"
    print("   ✓ Switched to Mistral Large 2 (European company)")

    # Example 6: Cost-effective option with Claude Haiku
    print("\n" + "=" * 80)
    print("Example 6: Claude 3.5 Haiku (Cost-Effective)")
    print("=" * 80)
    cognee.config.llm_model = "bedrock/anthropic.claude-3-5-haiku-20241022-v1:0"
    print("   ✓ Switched to Claude Haiku (fast and cost-effective)")

    print("\n" + "=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)
    print("\nKey Features Demonstrated:")
    print("  ✓ Native instructor[bedrock] integration")
    print("  ✓ Automatic BEDROCK_TOOLS mode for supported models")
    print("  ✓ Multiple model providers (Anthropic, Amazon, Meta, Mistral)")
    print("  ✓ Cross-region inference profiles")
    print("  ✓ Multimodal model support (Nova)")
    print("  ✓ Open-source models (Llama)")
    print("  ✓ European AI compliance (Mistral)")
    print("\nFor more models and configuration options, see docs/MODELS.md")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
