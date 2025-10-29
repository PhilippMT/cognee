"""AWS Bedrock LLM Adapter for Cognee"""

import asyncio
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

logger = get_logger("BedrockLLMAdapter")

# Constants
BEDROCK_PREFIX = 'bedrock/'


class BedrockLLMAdapter(LLMInterface):
    """
    Adapter for AWS Bedrock foundation models API using instructor[bedrock].

    This class initializes the AWS Bedrock API adapter with necessary credentials and configurations for
    interacting with AWS Bedrock foundation models. It provides methods for creating structured outputs
    based on user input and system prompts using instructor's native Bedrock integration.

    Uses boto3 client with instructor.from_bedrock() for direct AWS Bedrock integration.
    Async calls are handled using asyncio.to_thread() since boto3 doesn't support async natively.

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
        Initialize the BedrockLLMAdapter.

        Parameters:
        -----------
            model (str): The AWS Bedrock model identifier (e.g., 'anthropic.claude-3-7-sonnet-20250219-v1:0')
            max_completion_tokens (int): Maximum number of tokens in the completion
            aws_region_name (str): AWS region name (e.g., 'eu-central-1', 'eu-west-1')
            aws_access_key_id (str): AWS access key ID (optional, uses default credentials if not provided)
            aws_secret_access_key (str): AWS secret access key (optional)
            aws_profile_name (str): AWS named profile from ~/.aws/credentials (optional)
            fallback_model (str): Fallback model identifier
            fallback_aws_region_name (str): Fallback AWS region name
        """
        # Strip 'bedrock/' prefix as instructor handles it
        self.model = model.replace(BEDROCK_PREFIX, '') if model.startswith(BEDROCK_PREFIX) else model
        self.max_completion_tokens = max_completion_tokens
        self.aws_region_name = aws_region_name or "eu-central-1"
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_profile_name = aws_profile_name

        self.fallback_model = fallback_model.replace(BEDROCK_PREFIX, '') if fallback_model and fallback_model.startswith(BEDROCK_PREFIX) else fallback_model
        self.fallback_aws_region_name = fallback_aws_region_name

        # Create boto3 client with appropriate credentials
        session_kwargs = {'region_name': self.aws_region_name}
        if self.aws_profile_name:
            session_kwargs['profile_name'] = self.aws_profile_name
        
        session = boto3.Session(**session_kwargs)
        
        client_kwargs = {}
        if self.aws_access_key_id and self.aws_secret_access_key:
            client_kwargs['aws_access_key_id'] = self.aws_access_key_id
            client_kwargs['aws_secret_access_key'] = self.aws_secret_access_key
        
        self.bedrock_client = session.client('bedrock-runtime', **client_kwargs)
        
        # Initialize instructor client with boto3 bedrock client
        self.client = instructor.from_bedrock(self.bedrock_client)
        
        # Create fallback client if needed
        self.fallback_client = None
        if self.fallback_model and self.fallback_aws_region_name:
            fallback_session_kwargs = {'region_name': self.fallback_aws_region_name}
            if self.aws_profile_name:
                fallback_session_kwargs['profile_name'] = self.aws_profile_name
            
            fallback_session = boto3.Session(**fallback_session_kwargs)
            fallback_bedrock_client = fallback_session.client('bedrock-runtime', **client_kwargs)
            self.fallback_client = instructor.from_bedrock(fallback_bedrock_client)

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a response from a user query using AWS Bedrock.

        This asynchronous method sends a user query and a system prompt to an AWS Bedrock model and
        retrieves the generated response. Uses asyncio.to_thread to run synchronous Bedrock calls
        in a non-blocking way (AWS Bedrock SDK does not support async natively).

        Parameters:
        -----------
            text_input (str): The input text from the user to generate a response for.
            system_prompt (str): A prompt that provides context or instructions for the response generation.
            response_model (Type[BaseModel]): A Pydantic model that defines the structure of the expected response.

        Returns:
        --------
            BaseModel: An instance of the specified response model containing the structured output from the language model.
        """
        def _create_completion():
            """Synchronous function to call instructor client."""
            return self.client.chat.completions.create(
                modelId=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input},
                ],
                response_model=response_model,
                max_tokens=self.max_completion_tokens,
            )
        
        def _create_fallback_completion():
            """Synchronous function to call fallback instructor client."""
            if not self.fallback_client:
                raise RuntimeError("Fallback client not initialized")
            return self.fallback_client.chat.completions.create(
                modelId=self.fallback_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input},
                ],
                response_model=response_model,
                max_tokens=self.max_completion_tokens,
            )

        try:
            # Run synchronous Bedrock call in a thread pool to avoid blocking
            return await asyncio.to_thread(_create_completion)
            
        except InstructorRetryException as error:
            if "content management policy" not in str(error).lower():
                raise error

            if not (self.fallback_model and self.fallback_client):
                raise ContentPolicyFilterError(
                    f"The provided input contains content that is not aligned with our content policy: {text_input}"
                )

            # Try fallback model
            logger.warning(f"Primary model failed due to content policy. Trying fallback model: {self.fallback_model}")
            try:
                return await asyncio.to_thread(_create_fallback_completion)
            except InstructorRetryException as fallback_error:
                if "content management policy" not in str(fallback_error).lower():
                    raise fallback_error
                else:
                    raise ContentPolicyFilterError(
                        f"The provided input contains content that is not aligned with our content policy: {text_input}"
                    )
        except Exception as error:
            logger.error(f"Unexpected error in Bedrock LLM adapter: {str(error)}")
            raise error
