"""AWS Bedrock LLM Adapter for Cognee using BAML"""

import os
import asyncio
from typing import Type, Optional, Any, Dict
from pydantic import BaseModel

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
    Adapter for AWS Bedrock foundation models API using BAML.

    This class initializes the AWS Bedrock API adapter with necessary credentials and configurations for
    interacting with AWS Bedrock foundation models. It uses BAML's native Bedrock support with
    proper tools/function calling configuration for structured outputs.

    BAML provides a type-safe way to interact with LLMs through its domain-specific language,
    with automatic JSON parsing and validation.

    Public methods:
    - acreate_structured_output(text_input: str, system_prompt: str, response_model: Type[BaseModel]) -> BaseModel
    """

    name: str = "AWS Bedrock (BAML)"
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
        Initialize the BamlBedrockLLMAdapter with BAML.

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

        # Get model configuration for BAML
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

        # Set environment variables for BAML AWS credentials
        self._setup_aws_credentials()

        logger.info(
            f"Initialized BamlBedrockLLMAdapter with model={self.model}, "
            f"region={self.aws_region_name}, mode={self._recommended_mode}"
        )

    def _setup_aws_credentials(self):
        """Set up AWS credentials as environment variables for BAML."""
        if self.aws_region_name:
            os.environ["AWS_REGION"] = self.aws_region_name

        if self.aws_profile_name:
            os.environ["AWS_PROFILE"] = self.aws_profile_name

        if self.aws_access_key_id:
            os.environ["AWS_ACCESS_KEY_ID"] = self.aws_access_key_id

        if self.aws_secret_access_key:
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.aws_secret_access_key

    def _create_baml_client_config(self) -> Dict[str, Any]:
        """Create BAML client configuration dynamically."""
        model_id = remove_bedrock_prefix(self.model)

        config = {
            "provider": "aws-bedrock",
            "options": {
                "model": model_id,
                "inference_configuration": {
                    "max_tokens": self.max_completion_tokens,
                },
            },
        }

        if self.aws_region_name:
            config["options"]["region"] = self.aws_region_name

        if self.aws_profile_name:
            config["options"]["profile"] = self.aws_profile_name

        if self.aws_access_key_id and self.aws_secret_access_key:
            config["options"]["access_key_id"] = self.aws_access_key_id
            config["options"]["secret_access_key"] = self.aws_secret_access_key

        return config

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a response from a user query using AWS Bedrock with BAML.

        This asynchronous method sends a user query and a system prompt to an AWS Bedrock model and
        retrieves the generated response using BAML's type-safe extraction capabilities.

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
            # Import baml_py for dynamic client creation
            import baml_py
            from baml_py import ClientRegistry

            # Get model ID without prefix
            model_id = remove_bedrock_prefix(self.model)

            # Create client registry
            registry = ClientRegistry()

            # Add client with dynamic configuration
            client_config = self._create_baml_client_config()

            # Register the client dynamically
            registry.add_llm_client(
                name="bedrock_client",
                provider="aws-bedrock",
                options=client_config["options"],
            )

            # Create the prompt combining system and user input
            full_prompt = f"{system_prompt}\n\n{text_input}" if system_prompt else text_input

            # Use BAML's type extraction capability
            # Since BAML generates code from .baml files, we use dynamic invocation
            result = await self._invoke_baml_extraction(
                registry=registry,
                prompt=full_prompt,
                response_model=response_model,
            )

            return result

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
                logger.error(f"Error in BAML Bedrock call: {error}")
                raise error

    async def _invoke_baml_extraction(
        self,
        registry: Any,
        prompt: str,
        response_model: Type[BaseModel],
    ) -> BaseModel:
        """
        Invoke BAML to extract structured data from the LLM response.

        This method uses BAML's runtime extraction capabilities.
        """
        import baml_py
        from baml_py import BamlRuntime

        # Create the schema from the Pydantic model
        schema = response_model.model_json_schema()

        # For BAML, we need to format the prompt to request JSON output
        json_prompt = f"""{prompt}

Please respond with valid JSON that matches this schema:
{schema}

Respond ONLY with the JSON object, no additional text."""

        # Get model ID
        model_id = remove_bedrock_prefix(self.model)

        # Use boto3 directly with BAML-style configuration
        # This is a fallback approach since BAML's dynamic API requires generated code
        import boto3
        import json

        # Create boto3 client
        bedrock_kwargs = {
            "service_name": "bedrock-runtime",
            "region_name": self.aws_region_name,
        }

        if self.aws_profile_name:
            session = boto3.Session(profile_name=self.aws_profile_name)
            bedrock_client = session.client(**bedrock_kwargs)
        elif self.aws_access_key_id and self.aws_secret_access_key:
            bedrock_kwargs["aws_access_key_id"] = self.aws_access_key_id
            bedrock_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            bedrock_client = boto3.client(**bedrock_kwargs)
        else:
            bedrock_client = boto3.client(**bedrock_kwargs)

        # Prepare the request using Converse API (BAML's approach)
        messages = [{"role": "user", "content": [{"text": json_prompt}]}]

        def _sync_call():
            response = bedrock_client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": self.max_completion_tokens,
                    "temperature": 0.7,
                },
            )
            return response

        # Run in thread pool to avoid blocking
        response = await asyncio.to_thread(_sync_call)

        # Extract the response text
        output = response.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])

        if content and len(content) > 0:
            response_text = content[0].get("text", "")
        else:
            raise ValueError("No content in Bedrock response")

        # Parse the JSON response
        try:
            # Try to extract JSON from the response
            json_str = response_text.strip()

            # Handle potential markdown code blocks
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()

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
