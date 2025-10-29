# Migration to instructor[bedrock]

**Date:** October 29, 2025  
**Version:** 0.2.0

## Overview

This migration updates the `cognee-aws-bedrock` adapter to use the native `instructor[bedrock]` integration instead of the litellm-based approach. This provides better compatibility with AWS Bedrock's API and follows the official instructor documentation patterns.

## What Changed

### 1. Dependencies

**Before:**
```toml
dependencies = [
    "cognee>=0.1.0",
    "litellm>=1.0.0",
    "boto3>=1.34.0",
]
```

**After:**
```toml
dependencies = [
    "cognee>=0.1.0",
    "instructor[bedrock]>=1.0.0",
    "boto3>=1.34.0",
    "litellm>=1.0.0",  # Still needed for embeddings
]
```

### 2. LLM Adapter Implementation

**Key Changes:**

1. **Client Initialization:**
   - **Old:** `instructor.from_litellm(litellm.acompletion, mode=instructor.Mode.JSON)`
   - **New:** `instructor.from_bedrock(boto3_client)`

2. **Model ID Handling:**
   - Strip `bedrock/` prefix as instructor handles it internally
   - Example: `bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0` → `anthropic.claude-3-7-sonnet-20250219-v1:0`

3. **Async Pattern:**
   - AWS Bedrock SDK (boto3) doesn't support async natively
   - Use `asyncio.to_thread()` to run synchronous calls in non-blocking way
   ```python
   def _create_completion():
       return self.client.chat.completions.create(...)
   
   result = await asyncio.to_thread(_create_completion)
   ```

4. **Message Format:**
   - Use standard OpenAI-compatible format
   - System prompt first, then user message
   ```python
   messages=[
       {"role": "system", "content": system_prompt},
       {"role": "user", "content": text_input},
   ]
   ```

5. **API Parameters:**
   - Use `modelId` (Bedrock-native) instead of `model`
   - Configure region via boto3 Session, not in create call
   - Remove litellm-specific parameters like `aws_region_name` from create call

### 3. Credential Handling

**Improved boto3 Integration:**

```python
# Create session with profile if specified
session_kwargs = {'region_name': self.aws_region_name}
if self.aws_profile_name:
    session_kwargs['profile_name'] = self.aws_profile_name

session = boto3.Session(**session_kwargs)

# Add explicit credentials if provided
client_kwargs = {}
if self.aws_access_key_id and self.aws_secret_access_key:
    client_kwargs['aws_access_key_id'] = self.aws_access_key_id
    client_kwargs['aws_secret_access_key'] = self.aws_secret_access_key

bedrock_client = session.client('bedrock-runtime', **client_kwargs)
client = instructor.from_bedrock(bedrock_client)
```

### 4. Fallback Model Support

- Create separate boto3 clients for primary and fallback models
- Each with their own region and credentials
- Fallback client initialized at startup if configured

## What Stayed the Same

1. **Embedding Adapter:** Still uses litellm for embeddings (no change)
2. **Public API:** Same interface for users - `register_bedrock_adapters()`, config settings
3. **Model Support:** All models still work (Claude, Llama, Titan, Nova, etc.)
4. **Authentication:** Same AWS credential chain (profile, keys, IAM role)
5. **Error Handling:** Content policy filtering and fallback logic preserved

## Benefits

1. **Native Integration:** Direct boto3 → instructor flow without litellm intermediary
2. **Better Compatibility:** Follows official instructor[bedrock] patterns
3. **Simpler Debugging:** Fewer abstraction layers
4. **Type Safety:** Better type hints with native boto3 integration
5. **Future-Proof:** Aligned with instructor's recommended approach

## Migration Guide for Users

**No changes required for end users!** The public API remains the same:

```python
from cognee_aws_bedrock import register_bedrock_adapters
import cognee

# Same as before
register_bedrock_adapters()
cognee.config.llm_provider = "aws_bedrock"
cognee.config.llm_model = "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0"
await cognee.add("Your data")
await cognee.cognify()
```

## Testing Checklist

- [ ] LLM structured output generation works
- [ ] Embeddings still work (litellm)
- [ ] AWS credential chain (profile, keys, IAM role)
- [ ] Cross-region inference profiles
- [ ] Fallback model on content policy violation
- [ ] Error handling and retries
- [ ] Async operations don't block event loop

## References

- [Instructor Bedrock Integration](https://python.useinstructor.com/integrations/bedrock/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Boto3 Bedrock Runtime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## Troubleshooting

### Issue: "AttributeError: 'BedrockRuntimeClient' object has no attribute 'chat'"
**Solution:** Using `instructor.from_bedrock()` instead of trying to call boto3 client directly.

### Issue: "Event loop is closed" or blocking issues
**Solution:** Use `asyncio.to_thread()` to wrap synchronous Bedrock calls.

### Issue: Model ID format errors
**Solution:** Strip `bedrock/` prefix - instructor handles it automatically.

### Issue: Region not recognized
**Solution:** Configure region via boto3.Session, not in create call parameters.
