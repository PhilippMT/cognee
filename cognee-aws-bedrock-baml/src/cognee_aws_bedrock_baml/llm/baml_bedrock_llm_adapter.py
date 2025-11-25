"""AWS Bedrock LLM Adapter for Cognee using BAML-style configuration

This module provides an AWS Bedrock LLM adapter that follows BAML's configuration
patterns and uses the AWS Bedrock Converse API (the same API that BAML uses internally).

BAML (Boundary ML) is a DSL for type-safe LLM interactions. This adapter implements
a compatible approach using boto3's Converse API with BAML-style configuration,
allowing users to use the same model configurations defined in the .baml files.
"""

import os
import json
import asyncio
from typing import Type, Optional, Any, Dict
from pydantic import BaseModel
import boto3

from cognee.infrastructure.llm.exceptions import ContentPolicyFilterError
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.llm_interface import (
    LLMInterface,
)
from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.rate_limiter import (
    rate_limit_async,
    sleep_and_retry_async,
)
from cognee.shared.logging_utils import get_logger

from ..utils import ensure_bedrock_prefix, remove_bedrock_prefix
from ..bedrock_models_config import get_model_config, get_recommended_mode

logger = get_logger("BamlBedrockLLMAdapter")


class BamlBedrockLLMAdapter(LLMInterface):
    """
    Adapter for AWS Bedrock foundation models using BAML-style configuration.

    This adapter uses AWS Bedrock's Converse API (the same API that BAML uses internally)
    with configuration patterns matching BAML's aws-bedrock provider. It provides
    structured output extraction using JSON schema prompting and Pydantic validation.

    The included .baml files define client configurations that can be used with BAML's
    code generation, while this adapter provides a runtime-configurable alternative
    that follows the same patterns.

    Public methods:
    - acreate_structured_output(text_input: str, system_prompt: str, response_model: Type[BaseModel]) -> BaseModel
    """

    name: str = "AWS Bedrock (BAML-style)"
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
        Initialize the BamlBedrockLLMAdapter.

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
        self.aws_region_name = aws_region_name or os.environ.get("AWS_REGION", "eu-central-1")
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_profile_name = aws_profile_name

        self.fallback_model = fallback_model
        self.fallback_aws_region_name = fallback_aws_region_name

        # Get model configuration
        model_id_without_prefix = remove_bedrock_prefix(self.model)
        try:
            self._model_config = get_model_config(model_id_without_prefix)
            self._recommended_mode = get_recommended_mode(model_id_without_prefix)
        except ValueError:
            self._model_config = None
            self._recommended_mode = "json"
            logger.warning(
                f"Model {model_id_without_prefix} not found in configuration, "
                f"using default mode: json"
            )

        # Initialize the boto3 Bedrock client (BAML uses the same underlying API)
        self._bedrock_client = self._create_bedrock_client()

        logger.info(
            f"Initialized BamlBedrockLLMAdapter with model={self.model}, "
            f"region={self.aws_region_name}, mode={self._recommended_mode}"
        )

    def _create_bedrock_client(self):
        """Create boto3 Bedrock runtime client with proper credentials."""
        bedrock_kwargs = {
            "service_name": "bedrock-runtime",
            "region_name": self.aws_region_name,
        }

        if self.aws_profile_name:
            session = boto3.Session(profile_name=self.aws_profile_name)
            return session.client(**bedrock_kwargs)
        elif self.aws_access_key_id and self.aws_secret_access_key:
            bedrock_kwargs["aws_access_key_id"] = self.aws_access_key_id
            bedrock_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            return boto3.client(**bedrock_kwargs)
        else:
            return boto3.client(**bedrock_kwargs)

    def get_baml_config(self) -> Dict[str, Any]:
        """
        Get BAML-style configuration for this adapter.

        Returns a dictionary matching the BAML client configuration format,
        useful for reference or for generating .baml files.
        """
        model_id = remove_bedrock_prefix(self.model)

        config = {
            "provider": "aws-bedrock",
            "options": {
                "model": model_id,
                "inference_configuration": {
                    "max_tokens": self.max_completion_tokens,
                    "temperature": 0.7,
                },
            },
        }

        if self.aws_region_name:
            config["options"]["region"] = self.aws_region_name

        if self.aws_profile_name:
            config["options"]["profile"] = self.aws_profile_name

        return config

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a structured response using AWS Bedrock's Converse API.

        This method uses the same API that BAML's aws-bedrock provider uses internally,
        with JSON schema prompting for structured output extraction.

        Parameters:
        -----------
            text_input (str): The input text from the user to generate a response for.
            system_prompt (str): A prompt that provides context or instructions for the response generation.
            response_model (Type[BaseModel]): A Pydantic model that defines the structure of the expected response.

        Returns:
        --------
            BaseModel: An instance of the specified response model containing the structured output from the language model.
        """
        try:
            # Get model ID without prefix
            model_id = remove_bedrock_prefix(self.model)

            # Create the schema from the Pydantic model for structured output
            schema = response_model.model_json_schema()

            # Build the prompt with JSON schema instructions
            full_prompt = self._build_structured_prompt(
                text_input=text_input,
                system_prompt=system_prompt,
                schema=schema,
            )

            # Prepare messages for the Converse API
            messages = [{"role": "user", "content": [{"text": full_prompt}]}]

            # Call Bedrock using the Converse API (BAML's approach)
            response = await self._invoke_converse_api(
                model_id=model_id,
                messages=messages,
            )

            # Parse and validate the response
            return self._parse_response(response, response_model)

        except Exception as error:
            error_str = str(error).lower()

            # Check if it's a content policy violation
            if "content management policy" in error_str or "content policy" in error_str:
                if not (self.fallback_model and self.fallback_aws_region_name):
                    raise ContentPolicyFilterError(
                        f"The provided input contains content that is not aligned with our content policy: {text_input}"
                    )

                # Try fallback model
                return await self._try_fallback(
                    text_input=text_input,
                    system_prompt=system_prompt,
                    response_model=response_model,
                )
            else:
                logger.error(f"Error in BAML-style Bedrock call: {error}")
                raise error

    def _build_structured_prompt(
        self, text_input: str, system_prompt: str, schema: Dict[str, Any]
    ) -> str:
        """Build a prompt that requests JSON output matching the schema."""
        base_prompt = f"{system_prompt}\n\n{text_input}" if system_prompt else text_input

        return f"""{base_prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Respond ONLY with the JSON object, no additional text or markdown formatting."""

    async def _invoke_converse_api(
        self, model_id: str, messages: list
    ) -> Dict[str, Any]:
        """
        Invoke AWS Bedrock's Converse API asynchronously.

        This is the same API that BAML uses internally for aws-bedrock provider.
        """
        def _sync_call():
            return self._bedrock_client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": self.max_completion_tokens,
                    "temperature": 0.7,
                },
            )

        # Run sync call in thread pool to avoid blocking
        return await asyncio.to_thread(_sync_call)

    def _parse_response(
        self, response: Dict[str, Any], response_model: Type[BaseModel]
    ) -> BaseModel:
        """Parse the Bedrock response and validate against the Pydantic model."""
        # Extract the response text
        output = response.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])

        if content and len(content) > 0:
            response_text = content[0].get("text", "")
        else:
            raise ValueError("No content in Bedrock response")

        # Clean up the response text (handle markdown code blocks)
        json_str = response_text.strip()

        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()

        # Parse and validate
        try:
            parsed_data = json.loads(json_str)
            return response_model.model_validate(parsed_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response_text}")
            raise ValueError(f"Invalid JSON in response: {e}")

    async def _try_fallback(
        self,
        text_input: str,
        system_prompt: str,
        response_model: Type[BaseModel],
    ) -> BaseModel:
        """Try the fallback model when the primary model fails."""
        logger.warning(
            f"Primary model failed, trying fallback model: {self.fallback_model} "
            f"in region: {self.fallback_aws_region_name}"
        )

        # Create a new adapter with the fallback configuration
        fallback_adapter = BamlBedrockLLMAdapter(
            model=self.fallback_model,
            max_completion_tokens=self.max_completion_tokens,
            aws_region_name=self.fallback_aws_region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_profile_name=self.aws_profile_name,
            fallback_model=None,  # No further fallback
            fallback_aws_region_name=None,
        )

        try:
            return await fallback_adapter.acreate_structured_output(
                text_input=text_input,
                system_prompt=system_prompt,
                response_model=response_model,
            )
        except Exception as fallback_error:
            error_str = str(fallback_error).lower()
            if "content management policy" in error_str or "content policy" in error_str:
                raise ContentPolicyFilterError(
                    f"The provided input contains content that is not aligned with our content policy: {text_input}"
                )
            else:
                raise fallback_error
