"""Adapter for AWS Bedrock foundation models API"""

import litellm
import instructor
from typing import Type
from pydantic import BaseModel
from openai import ContentFilterFinishReasonError
from litellm.exceptions import ContentPolicyViolationError
from instructor.exceptions import InstructorRetryException

from cognee.infrastructure.llm.exceptions import ContentPolicyFilterError
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.llm_interface import (
    LLMInterface,
)
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.rate_limiter import (
    rate_limit_async,
    sleep_and_retry_async,
)


class BedrockAdapter(LLMInterface):
    """
    Adapter for AWS Bedrock foundation models API.

    This class initializes the AWS Bedrock API adapter with necessary credentials and configurations for
    interacting with AWS Bedrock foundation models. It provides methods for creating structured outputs
    based on user input and system prompts using litellm.

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
        fallback_model: str = None,
        fallback_aws_region_name: str = None,
    ):
        """
        Initialize the BedrockAdapter.

        Parameters:
        -----------
            model (str): The AWS Bedrock model identifier (e.g., 'bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0')
            max_completion_tokens (int): Maximum number of tokens in the completion
            aws_region_name (str): AWS region name (e.g., 'eu-central-1', 'eu-west-1')
            aws_access_key_id (str): AWS access key ID (optional, uses default credentials if not provided)
            aws_secret_access_key (str): AWS secret access key (optional)
            fallback_model (str): Fallback model identifier
            fallback_aws_region_name (str): Fallback AWS region name
        """
        self.model = model if model.startswith("bedrock/") else f"bedrock/{model}"
        self.max_completion_tokens = max_completion_tokens
        self.aws_region_name = aws_region_name or "eu-central-1"
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

        self.fallback_model = fallback_model
        self.fallback_aws_region_name = fallback_aws_region_name

        # Initialize instructor client with litellm
        # AWS Bedrock models work with JSON mode in litellm
        self.aclient = instructor.from_litellm(
            litellm.acompletion, mode=instructor.Mode.JSON
        )

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a response from a user query using AWS Bedrock.

        This asynchronous method sends a user query and a system prompt to an AWS Bedrock model and
        retrieves the generated response. It handles API communication and retries up to a
        specified limit in case of request failures.

        Parameters:
        -----------
            text_input (str): The input text from the user to generate a response for.
            system_prompt (str): A prompt that provides context or instructions for the response generation.
            response_model (Type[BaseModel]): A Pydantic model that defines the structure of the expected response.

        Returns:
        --------
            BaseModel: An instance of the specified response model containing the structured output from the language model.
        """
        # Prepare AWS credentials if provided
        extra_params = {}
        if self.aws_access_key_id:
            extra_params["aws_access_key_id"] = self.aws_access_key_id
        if self.aws_secret_access_key:
            extra_params["aws_secret_access_key"] = self.aws_secret_access_key

        try:
            return await self.aclient.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": f"""{text_input}""",
                    },
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                ],
                max_retries=5,
                aws_region_name=self.aws_region_name,
                response_model=response_model,
                **extra_params,
            )
        except (
            ContentFilterFinishReasonError,
            ContentPolicyViolationError,
            InstructorRetryException,
        ) as error:
            if (
                isinstance(error, InstructorRetryException)
                and "content management policy" not in str(error).lower()
            ):
                raise error

            if not (self.fallback_model and self.fallback_aws_region_name):
                raise ContentPolicyFilterError(
                    f"The provided input contains content that is not aligned with our content policy: {text_input}"
                )

            # Try fallback model
            fallback_model = (
                self.fallback_model
                if self.fallback_model.startswith("bedrock/")
                else f"bedrock/{self.fallback_model}"
            )

            try:
                return await self.aclient.chat.completions.create(
                    model=fallback_model,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""{text_input}""",
                        },
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                    ],
                    max_retries=5,
                    aws_region_name=self.fallback_aws_region_name,
                    response_model=response_model,
                    **extra_params,
                )
            except (
                ContentFilterFinishReasonError,
                ContentPolicyViolationError,
                InstructorRetryException,
            ) as error:
                if (
                    isinstance(error, InstructorRetryException)
                    and "content management policy" not in str(error).lower()
                ):
                    raise error
                else:
                    raise ContentPolicyFilterError(
                        f"The provided input contains content that is not aligned with our content policy: {text_input}"
                    )
