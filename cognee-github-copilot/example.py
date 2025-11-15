"""
Example usage of GitHub Copilot adapter with Cognee.

This example demonstrates how to use GitHub Copilot models with Cognee
for building a knowledge graph from text data.
"""

import asyncio
import cognee
from cognee_github_copilot import register_github_copilot_adapters


async def main():
    """Main example function."""
    
    # Step 1: Register GitHub Copilot adapters
    print("Step 1: Registering GitHub Copilot adapters...")
    register_github_copilot_adapters()
    
    # Step 2: Configure GitHub Copilot as LLM provider
    print("\nStep 2: Configuring GitHub Copilot...")
    cognee.config.llm_provider = "github_copilot"
    
    # Try different models - uncomment to test different models:
    
    # OpenAI Models
    cognee.config.llm_model = "gpt-4o"  # Fast, multimodal
    # cognee.config.llm_model = "gpt-4.1"  # Advanced reasoning
    # cognee.config.llm_model = "gpt-5"  # Next-gen (preview)
    # cognee.config.llm_model = "gpt-5-mini"  # Lightweight
    # cognee.config.llm_model = "o3"  # Extended reasoning
    # cognee.config.llm_model = "o4-mini"  # Balanced reasoning
    
    # Anthropic Models
    # cognee.config.llm_model = "claude-sonnet-4"  # Latest balanced
    # cognee.config.llm_model = "claude-sonnet-3.7"  # Enhanced
    # cognee.config.llm_model = "claude-sonnet-3.5"  # Classic
    # cognee.config.llm_model = "claude-opus-4"  # Top-tier
    # cognee.config.llm_model = "claude-opus-4.1"  # Highest capability
    
    # Google Models
    # cognee.config.llm_model = "gemini-2.5-pro"  # 1M+ context
    # cognee.config.llm_model = "gemini-2.0-flash"  # Fast & efficient
    
    # xAI Models
    # cognee.config.llm_model = "grok-code-fast-1"  # Code-optimized
    
    print(f"Using model: {cognee.config.llm_model}")
    
    # Step 3: Configure embeddings (GitHub Copilot doesn't provide embeddings)
    print("\nStep 3: Configuring embeddings...")
    cognee.config.embedding_provider = "openai"
    cognee.config.embedding_model = "text-embedding-3-small"
    cognee.config.embedding_dimensions = 1536
    
    # Step 4: Clean up any existing data
    print("\nStep 4: Cleaning up existing data...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # Step 5: Add sample data
    print("\nStep 5: Adding sample data...")
    sample_text = """
    Artificial Intelligence (AI) is transforming software development.
    GitHub Copilot uses large language models to assist developers with code generation.
    Modern AI systems like GPT-4, Claude, and Gemini can understand context and generate human-like text.
    These models are trained on vast amounts of data and can perform various tasks including:
    - Code completion and generation
    - Natural language understanding
    - Problem-solving and reasoning
    - Multi-modal processing (text, images, audio)
    
    The integration of AI into development tools has significantly increased developer productivity.
    """
    
    await cognee.add([sample_text], "ai_knowledge")
    print("✓ Data added successfully")
    
    # Step 6: Process data with cognify
    print("\nStep 6: Running cognify to build knowledge graph...")
    await cognee.cognify(["ai_knowledge"])
    print("✓ Knowledge graph built successfully")
    
    # Step 7: Search the knowledge graph
    print("\nStep 7: Searching knowledge graph...")
    
    queries = [
        "What is GitHub Copilot?",
        "What can AI models do?",
        "How does AI help developers?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = await cognee.search(query)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {str(result)[:200]}...")
    
    print("\n✓ Example completed successfully!")


async def example_with_custom_api_key():
    """Example with custom API key."""
    print("Example with custom API key:")
    
    # Register with custom API key
    register_github_copilot_adapters(
        api_key="your-github-token-here"
    )
    
    cognee.config.llm_provider = "github_copilot"
    cognee.config.llm_model = "claude-sonnet-4"
    
    # Rest of the code is the same...
    print("✓ Configured with custom API key")


async def example_model_comparison():
    """Example comparing different models."""
    print("\nExample: Model Comparison")
    print("=" * 60)
    
    models = [
        ("gpt-4o", "Fast, multimodal"),
        ("claude-sonnet-4", "Latest balanced"),
        ("gemini-2.0-flash", "Fast & efficient"),
    ]
    
    test_data = "Python is a high-level programming language known for its simplicity and readability."
    
    for model_name, description in models:
        print(f"\nTesting {model_name} ({description})...")
        
        # Configure model
        cognee.config.llm_model = model_name
        
        # Clean and add data
        await cognee.prune.prune_data()
        await cognee.add([test_data], f"test_{model_name}")
        
        # Process
        await cognee.cognify([f"test_{model_name}"])
        
        # Search
        results = await cognee.search("What is Python?")
        print(f"  Results: {len(results)}")
        
    print("\n✓ Model comparison completed")


if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Copilot Adapter Example")
    print("=" * 60)
    
    # Run main example
    asyncio.run(main())
    
    # Uncomment to run other examples:
    # asyncio.run(example_with_custom_api_key())
    # asyncio.run(example_model_comparison())
