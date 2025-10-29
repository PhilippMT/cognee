"""
Test script for instructor[bedrock] migration.

This script verifies that the migrated BedrockLLMAdapter works correctly
with the new instructor[bedrock] implementation.
"""

import asyncio
from typing import List
from pydantic import BaseModel


class TestOutput(BaseModel):
    """Simple test output model."""
    summary: str
    key_points: List[str]


async def test_bedrock_adapter():
    """Test the BedrockLLMAdapter with a simple structured output."""
    from cognee_aws_bedrock.llm.bedrock_llm_adapter import BedrockLLMAdapter
    
    # Initialize adapter
    adapter = BedrockLLMAdapter(
        model="anthropic.claude-3-haiku-20240307-v1:0",  # Fast, cost-effective model for testing
        max_completion_tokens=1024,
        aws_region_name="eu-central-1",
        # Uses default AWS credentials (profile, env vars, or IAM role)
    )
    
    print("✓ BedrockLLMAdapter initialized successfully")
    print(f"  Model: {adapter.model}")
    print(f"  Region: {adapter.aws_region_name}")
    
    # Test structured output
    text_input = "AWS Bedrock is a fully managed service that provides access to foundation models from leading AI companies."
    system_prompt = "Extract a summary and 2-3 key points from the text."
    
    print("\n🔄 Testing structured output generation...")
    print(f"  Input: {text_input[:60]}...")
    
    try:
        result = await adapter.acreate_structured_output(
            text_input=text_input,
            system_prompt=system_prompt,
            response_model=TestOutput
        )
        
        print("\n✅ Structured output generated successfully!")
        print(f"  Summary: {result.summary}")
        print("  Key Points:")
        for i, point in enumerate(result.key_points, 1):
            print(f"    {i}. {point}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fallback_model():
    """Test fallback model configuration."""
    from cognee_aws_bedrock.llm.bedrock_llm_adapter import BedrockLLMAdapter
    
    print("\n🔄 Testing fallback model configuration...")
    
    adapter = BedrockLLMAdapter(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_completion_tokens=1024,
        aws_region_name="eu-central-1",
        fallback_model="anthropic.claude-3-sonnet-20240229-v1:0",
        fallback_aws_region_name="eu-west-1"
    )
    
    print("✓ Fallback model configured")
    print(f"  Primary: {adapter.model} ({adapter.aws_region_name})")
    print(f"  Fallback: {adapter.fallback_model} ({adapter.fallback_aws_region_name})")
    print(f"  Fallback client initialized: {adapter.fallback_client is not None}")
    
    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing instructor[bedrock] Migration")
    print("=" * 60)
    
    # Test basic adapter
    success = await test_bedrock_adapter()
    
    # Test fallback configuration
    await test_fallback_model()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed - check AWS credentials and model access")
    print("=" * 60)


if __name__ == "__main__":
    print("\nNote: This test requires:")
    print("  1. AWS credentials configured (profile, env vars, or IAM role)")
    print("  2. Access to Claude models in AWS Bedrock")
    print("  3. Proper IAM permissions for bedrock:InvokeModel")
    print()
    
    asyncio.run(main())
