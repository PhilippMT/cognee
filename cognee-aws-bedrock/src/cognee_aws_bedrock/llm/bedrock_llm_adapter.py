"""AWS Bedrock LLM Adapter for Cognee"""

import boto3
import instructor
from typing import Type, Optional
from pydantic import BaseModel
from instructor.exceptions import InstructorRetryException

from cognee.infrastructure.llm.exceptions import ContentPolicyFilterError
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.llm_interface import (
    LLMInterface,
)
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.rate_limiter import (
    rate_limit_async,
    sleep_and_retry_async,
)
from cognee.shared.logging_utils import get_logger

from ..utils import ensure_bedrock_prefix
from ..bedrock_models_config import get_model_config, get_recommended_mode

logger = get_logger("BedrockLLMAdapter")


class BedrockLLMAdapter(LLMInterface):
    """
    Adapter for AWS Bedrock foundation models API using instructor[bedrock].

    This class initializes the AWS Bedrock API adapter with necessary credentials and configurations for
    interacting with AWS Bedrock foundation models. It uses instructor's native Bedrock support with
    proper tools/function calling configuration for structured outputs.

    Public methods:
    - acreate_structured_output(text_input: str, system_prompt: str, response_model: Type[BaseModel]) -> BaseModel
    """

    name: str = "AWS Bedrock"
    model: str
    aws_region_name: str

    def __init__(
        self,
        model: str,
        max_completion_tokens: int,
        aws_region_name: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_profile_name: str = None,
        fallback_model: str = None,
        fallback_aws_region_name: str = None,
    ):
        """
        Initialize the BedrockLLMAdapter with instructor[bedrock].

        Parameters:
        -----------
            model (str): The AWS Bedrock model identifier (e.g., 'anthropic.claude-3-5-sonnet-20241022-v2:0')
            max_completion_tokens (int): Maximum number of tokens in the completion
            aws_region_name (str): AWS region name (e.g., 'eu-central-1', 'eu-north-1')
            aws_access_key_id (str): AWS access key ID (optional, uses default credentials if not provided)
            aws_secret_access_key (str): AWS secret access key (optional)
            aws_profile_name (str): AWS named profile from ~/.aws/credentials (optional)
            fallback_model (str): Fallback model identifier
            fallback_aws_region_name (str): Fallback AWS region name
        """
        self.model = ensure_bedrock_prefix(model)
        self.max_completion_tokens = max_completion_tokens
        self.aws_region_name = aws_region_name or "eu-central-1"
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_profile_name = aws_profile_name

        self.fallback_model = fallback_model
        self.fallback_aws_region_name = fallback_aws_region_name

        # Determine the best mode for this model
        model_id_without_prefix = self.model.replace("bedrock/", "")
        try:
            recommended_mode = get_recommended_mode(model_id_without_prefix)
            if recommended_mode == "BEDROCK_TOOLS":
                self.mode = instructor.Mode.BEDROCK_TOOLS
            elif recommended_mode == "BEDROCK_JSON":
                self.mode = instructor.Mode.BEDROCK_JSON
            else:
                self.mode = instructor.Mode.JSON
        except ValueError:
            # Default to BEDROCK_JSON for unknown models
            self.mode = instructor.Mode.BEDROCK_JSON
            logger.warning(
                f"Model {model_id_without_prefix} not found in configuration, "
                f"using default mode: BEDROCK_JSON"
            )

        # Initialize boto3 Bedrock runtime client with credentials
        bedrock_kwargs = {
            "service_name": "bedrock-runtime",
            "region_name": self.aws_region_name,
        }
        
        if aws_profile_name:
            # Use named profile
            session = boto3.Session(profile_name=aws_profile_name)
            bedrock_client = session.client(**bedrock_kwargs)
        elif aws_access_key_id and aws_secret_access_key:
            # Use explicit credentials
            bedrock_kwargs["aws_access_key_id"] = aws_access_key_id
            bedrock_kwargs["aws_secret_access_key"] = aws_secret_access_key
            bedrock_client = boto3.client(**bedrock_kwargs)
        else:
            # Use default credential chain
            bedrock_client = boto3.client(**bedrock_kwargs)

        # Initialize instructor client with native Bedrock support
        self.aclient = instructor.from_bedrock(
            bedrock_client,
            mode=self.mode,
        )
        
        logger.info(
            f"Initialized BedrockLLMAdapter with model={self.model}, "
            f"region={self.aws_region_name}, mode={self.mode}"
        )

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a response from a user query using AWS Bedrock with instructor[bedrock].

        This asynchronous method sends a user query and a system prompt to an AWS Bedrock model and
        retrieves the generated response using instructor's native Bedrock support with proper
        tools/function calling configuration.

        Parameters:
        -----------
            text_input (str): The input text from the user to generate a response for.
            system_prompt (str): A prompt that provides context or instructions for the response generation.
            response_model (Type[BaseModel]): A Pydantic model that defines the structure of the expected response.

        Returns:
        --------
            BaseModel: An instance of the specified response model containing the structured output from the language model.
        """
        # Prepare messages in Bedrock format
        messages = [
            {
                "role": "user",
                "content": text_input,
            }
        ]
        
        # Add system prompt as a system message (Bedrock supports system messages)
        if system_prompt:
            messages.insert(0, {
                "role": "system",
                "content": system_prompt,
            })

        # Get model ID without bedrock/ prefix
        model_id = self.model.replace("bedrock/", "")

        try:
            # Use instructor's Bedrock integration with proper parameters
            # Note: instructor.from_bedrock uses synchronous API, so we need to wrap it
            # AWS Bedrock SDK (boto3) doesn't support async natively
            import asyncio
            
            def _sync_call():
                return self.aclient.chat.completions.create(
                    modelId=model_id,
                    messages=messages,
                    response_model=response_model,
                    max_retries=5,
                    inferenceConfig={
                        "maxTokens": self.max_completion_tokens,
                    }
                )
            
            # Run sync call in thread pool to avoid blocking
            result = await asyncio.to_thread(_sync_call)
            return result
            
        except InstructorRetryException as error:
            # Check if it's a content policy violation
            if "content management policy" in str(error).lower():
                if not (self.fallback_model and self.fallback_aws_region_name):
                    raise ContentPolicyFilterError(
                        f"The provided input contains content that is not aligned with our content policy: {text_input}"
                    )

                # Try fallback model
                fallback_model_id = (
                    self.fallback_model
                    if not self.fallback_model.startswith("bedrock/")
                    else self.fallback_model.replace("bedrock/", "")
                )

                # Create fallback client with different region
                fallback_bedrock_kwargs = {
                    "service_name": "bedrock-runtime",
                    "region_name": self.fallback_aws_region_name,
                }
                
                if self.aws_profile_name:
                    session = boto3.Session(profile_name=self.aws_profile_name)
                    fallback_bedrock_client = session.client(**fallback_bedrock_kwargs)
                elif self.aws_access_key_id and self.aws_secret_access_key:
                    fallback_bedrock_kwargs["aws_access_key_id"] = self.aws_access_key_id
                    fallback_bedrock_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
                    fallback_bedrock_client = boto3.client(**fallback_bedrock_kwargs)
                else:
                    fallback_bedrock_client = boto3.client(**fallback_bedrock_kwargs)

                fallback_client = instructor.from_bedrock(
                    fallback_bedrock_client,
                    mode=self.mode,
                )

                try:
                    def _sync_fallback_call():
                        return fallback_client.chat.completions.create(
                            modelId=fallback_model_id,
                            messages=messages,
                            response_model=response_model,
                            max_retries=5,
                            inferenceConfig={
                                "maxTokens": self.max_completion_tokens,
                            }
                        )
                    
                    result = await asyncio.to_thread(_sync_fallback_call)
                    return result
                    
                except InstructorRetryException as fallback_error:
                    if "content management policy" in str(fallback_error).lower():
                        raise ContentPolicyFilterError(
                            f"The provided input contains content that is not aligned with our content policy: {text_input}"
                        )
                    else:
                        raise fallback_error
            else:
                raise error
