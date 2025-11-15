"""GitHub Copilot LLM Adapter for Cognee"""

import litellm
import instructor
from typing import Type, Optional
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
from cognee.shared.logging_utils import get_logger

from ..utils import ensure_github_copilot_prefix

logger = get_logger("GitHubCopilotLLMAdapter")


class GitHubCopilotLLMAdapter(LLMInterface):
    """
    Adapter for GitHub Copilot API.

    This class initializes the GitHub Copilot API adapter with necessary credentials and configurations for
    interacting with GitHub Copilot models. It provides methods for creating structured outputs
    based on user input and system prompts using litellm with instructor.

    GitHub Copilot Pro+ supports multiple model providers:
    - OpenAI: GPT-4.1, GPT-4o, GPT-5, GPT-5 mini, o3, o4-mini
    - Anthropic: Claude Opus 4.1, Claude Opus 4, Claude Sonnet 3.5/3.7/4
    - Google: Gemini 2.5 Pro, Gemini 2.0 Flash
    - xAI: Grok Code Fast 1

    Public methods:
    - acreate_structured_output(text_input: str, system_prompt: str, response_model: Type[BaseModel]) -> BaseModel
    """

    name: str = "GitHub Copilot"
    model: str
    api_key: Optional[str]

    def __init__(
        self,
        model: str,
        max_completion_tokens: int,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        fallback_model: str = None,
        fallback_api_key: str = None,
    ):
        """
        Initialize the GitHubCopilotLLMAdapter.

        Parameters:
        -----------
            model (str): The GitHub Copilot model identifier (e.g., 'gpt-4o', 'claude-sonnet-3.5', 'gemini-2.0-flash')
            max_completion_tokens (int): Maximum number of tokens in the completion
            api_key (str, optional): GitHub Copilot API key (uses GITHUB_TOKEN from environment if not provided)
            endpoint (str, optional): Custom endpoint URL for GitHub Copilot API
            fallback_model (str): Fallback model identifier
            fallback_api_key (str): Fallback API key
        """
        self.model = ensure_github_copilot_prefix(model)
        self.max_completion_tokens = max_completion_tokens
        self.api_key = api_key
        self.endpoint = endpoint

        self.fallback_model = fallback_model
        self.fallback_api_key = fallback_api_key

        # Initialize instructor client with litellm
        # GitHub Copilot models work with JSON mode in litellm
        self.aclient = instructor.from_litellm(
            litellm.acompletion, mode=instructor.Mode.JSON
        )

    @sleep_and_retry_async()
    @rate_limit_async
    async def acreate_structured_output(
        self, text_input: str, system_prompt: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generate a response from a user query using GitHub Copilot.

        This asynchronous method sends a user query and a system prompt to a GitHub Copilot model and
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
        # Prepare request parameters
        request_params = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": f"""{text_input}""",
                },
                {
                    "role": "system",
                    "content": system_prompt,
                },
            ],
            "max_retries": 5,
            "response_model": response_model,
        }

        # Add optional parameters
        if self.api_key:
            request_params["api_key"] = self.api_key
        if self.endpoint:
            request_params["base_url"] = self.endpoint

        # Add GitHub Copilot specific headers
        request_params["extra_headers"] = {
            "editor-version": "vscode/1.85.1",
            "Copilot-Integration-Id": "vscode-chat"
        }

        try:
            return await self.aclient.chat.completions.create(**request_params)
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

            if not (self.fallback_model and self.fallback_api_key):
                raise ContentPolicyFilterError(
                    f"The provided input contains content that is not aligned with our content policy: {text_input}"
                )

            # Try fallback model
            fallback_model = (
                self.fallback_model
                if self.fallback_model.startswith("github_copilot/")
                else f"github_copilot/{self.fallback_model}"
            )

            fallback_params = request_params.copy()
            fallback_params["model"] = fallback_model
            fallback_params["api_key"] = self.fallback_api_key

            try:
                return await self.aclient.chat.completions.create(**fallback_params)
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
