"""AWS Bedrock Embedding Adapter for Cognee"""

import os
import asyncio
import math
from typing import List, Optional
import numpy as np
import litellm

from cognee.shared.logging_utils import get_logger
from cognee.infrastructure.databases.vector.embeddings.EmbeddingEngine import EmbeddingEngine
from cognee.infrastructure.databases.exceptions import EmbeddingException
from cognee.infrastructure.llm.tokenizer.TikToken import TikTokenTokenizer
from cognee.infrastructure.databases.vector.embeddings.embedding_rate_limiter import (
    embedding_rate_limit_async,
    embedding_sleep_and_retry_async,
)

from ..utils import ensure_bedrock_prefix

litellm.set_verbose = False
logger = get_logger("BedrockEmbeddingAdapter")


class BedrockEmbeddingAdapter(EmbeddingEngine):
    """
    AWS Bedrock Embedding Adapter for Cognee.
    
    Supports AWS Bedrock embedding models:
    - Amazon Titan Embed Text v1 & v2
    - Amazon Titan Embed Image v1 (Multimodal)
    - Cohere Embed English v3 & Multilingual v3/v4
    """

    api_key: str
    model: str
    dimensions: int
    mock: bool
    aws_region_name: str
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_profile_name: Optional[str]

    MAX_RETRIES = 5

    def __init__(
        self,
        model: str = "bedrock/amazon.titan-embed-text-v2:0",
        dimensions: int = 1024,
        max_completion_tokens: int = 8191,
        aws_region_name: str = "eu-central-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_profile_name: Optional[str] = None,
    ):
        """
        Initialize the BedrockEmbeddingAdapter.
        
        Parameters:
        -----------
            model (str): AWS Bedrock embedding model (e.g., 'bedrock/amazon.titan-embed-text-v2:0')
            dimensions (int): Embedding dimensions
            max_completion_tokens (int): Maximum tokens per request
            aws_region_name (str): AWS region
            aws_access_key_id (str): AWS access key (optional)
            aws_secret_access_key (str): AWS secret key (optional)
            aws_profile_name (str): AWS profile name (optional)
        """
        # Ensure model has bedrock/ prefix
        self.model = ensure_bedrock_prefix(model)
        self.dimensions = dimensions
        self.max_completion_tokens = max_completion_tokens
        self.aws_region_name = aws_region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_profile_name = aws_profile_name

        # Log initialization parameters
        logger.info(f"Initializing BedrockEmbeddingAdapter with parameters:")
        logger.info(f"  model: {self.model}")
        logger.info(f"  dimensions: {self.dimensions}")
        logger.info(f"  max_completion_tokens: {self.max_completion_tokens}")
        logger.info(f"  aws_region_name: {self.aws_region_name}")
        logger.info(f"  aws_profile_name: {self.aws_profile_name}")

        # Note: TikTokenizer with model=None may not provide accurate tokenization
        # for Bedrock models. Consider implementing Bedrock-specific tokenization
        # or using model-specific tokenizers in the future.
        self.tokenizer = TikTokenTokenizer(model=None, max_completion_tokens=max_completion_tokens)
        self.retry_count = 0

        enable_mocking = os.getenv("MOCK_EMBEDDING", "false")
        if isinstance(enable_mocking, bool):
            enable_mocking = str(enable_mocking).lower()
        self.mock = enable_mocking in ("true", "1", "yes")

    @embedding_sleep_and_retry_async()
    @embedding_rate_limit_async
    async def embed_text(self, text: List[str]) -> List[List[float]]:
        """
        Embed a list of text strings using AWS Bedrock.
        
        Parameters:
        -----------
            text (List[str]): A list of strings to be embedded.
            
        Returns:
        --------
            List[List[float]]: A list of vectors representing the embedded texts.
        """
        try:
            if self.mock:
                response = {"data": [{"embedding": [0.0] * self.dimensions} for _ in text]}
                return [data["embedding"] for data in response["data"]]
            else:
                # Prepare kwargs for litellm.aembedding
                embedding_kwargs = {
                    "model": self.model,
                    "input": text,
                    "aws_region_name": self.aws_region_name,
                }
                
                # Add AWS authentication parameters
                if self.aws_profile_name:
                    embedding_kwargs["aws_profile_name"] = self.aws_profile_name
                if self.aws_access_key_id:
                    embedding_kwargs["aws_access_key_id"] = self.aws_access_key_id
                if self.aws_secret_access_key:
                    embedding_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
                
                response = await litellm.aembedding(**embedding_kwargs)
                return [data["embedding"] for data in response.data]

        except litellm.exceptions.ContextWindowExceededError as error:
            if isinstance(text, list) and len(text) > 1:
                mid = math.ceil(len(text) / 2)
                left, right = text[:mid], text[mid:]
                left_vecs, right_vecs = await asyncio.gather(
                    self.embed_text(left),
                    self.embed_text(right),
                )
                return left_vecs + right_vecs

            if isinstance(text, list) and len(text) == 1:
                logger.debug(f"Pooling embeddings of text string with size: {len(text[0])}")
                s = text[0]
                third = len(s) // 3
                left_part, right_part = s[: third * 2], s[third:]

                (left_vec,), (right_vec,) = await asyncio.gather(
                    self.embed_text([left_part]),
                    self.embed_text([right_part]),
                )

                pooled = (np.array(left_vec) + np.array(right_vec)) / 2
                return [pooled.tolist()]

            logger.error("Context window exceeded for embedding text: %s", str(error))
            raise error

        except (
            litellm.exceptions.BadRequestError,
            litellm.exceptions.NotFoundError,
        ) as e:
            logger.error(f"Embedding error with model {self.model}: {str(e)}")
            raise EmbeddingException(f"Failed to index data points using model {self.model}")

        except Exception as error:
            logger.error("Error embedding text: %s", str(error))
            raise error

    def get_vector_size(self) -> int:
        """
        Retrieve the dimensionality of the embedding vectors.
        
        Returns:
        --------
            int: The size (dimensionality) of the embedding vectors.
        """
        return self.dimensions

    def get_tokenizer(self):
        """
        Load and return the appropriate tokenizer.
        
        Returns:
        --------
            The tokenizer instance compatible with the model.
        """
        return self.tokenizer
