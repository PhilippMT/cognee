"""Content processor using Jina ReaderLM-v2."""

import os
import re
import logging
from typing import Dict, List, Optional
from openai import AsyncOpenAI


logger = logging.getLogger(__name__)


class ContentProcessor:
    """
    Process HTML content using ReaderLM-v2 for extraction.
    
    Uses vLLM server with OpenAI-compatible API for:
    - HTML to Markdown conversion
    - Fact extraction
    - Content cleaning
    """
    
    # HTML cleaning patterns
    SCRIPT_PATTERN = re.compile(r"<[ ]*script.*?\/[ ]*script[ ]*>", re.DOTALL | re.IGNORECASE)
    STYLE_PATTERN = re.compile(r"<[ ]*style.*?\/[ ]*style[ ]*>", re.DOTALL | re.IGNORECASE)
    META_PATTERN = re.compile(r"<[ ]*meta.*?>", re.IGNORECASE)
    COMMENT_PATTERN = re.compile(r"<[ ]*!--.*?--[ ]*>", re.DOTALL)
    LINK_PATTERN = re.compile(r"<[ ]*link.*?>", re.IGNORECASE)
    BASE64_IMG_PATTERN = re.compile(r'<img[^>]+src="data:image/[^;]+;base64,[^"]+"[^>]*>')
    SVG_PATTERN = re.compile(r"(<svg[^>]*>)(.*?)(<\/svg>)", re.DOTALL | re.IGNORECASE)
    
    def __init__(self):
        """Initialize ReaderLM-v2 client."""
        self.api_base = os.getenv("VLLM_API_BASE", "http://localhost:8000/v1")
        self.model_name = os.getenv("VLLM_MODEL_NAME", "jinaai/ReaderLM-v2")
        
        self.client = AsyncOpenAI(
            base_url=self.api_base,
            api_key=os.getenv("VLLM_API_KEY", "token-abc123"),
        )
        
        logger.info(f"Initialized ContentProcessor with {self.model_name} at {self.api_base}")
    
    def clean_html(self, html: str) -> str:
        """
        Pre-clean HTML to reduce noise.
        
        Removes:
        - Scripts and styles
        - Meta tags and links
        - HTML comments
        - Base64 images
        - Complex SVGs
        """
        # Remove scripts
        html = self.SCRIPT_PATTERN.sub("", html)
        
        # Remove styles
        html = self.STYLE_PATTERN.sub("", html)
        
        # Remove meta tags
        html = self.META_PATTERN.sub("", html)
        
        # Remove comments
        html = self.COMMENT_PATTERN.sub("", html)
        
        # Remove link tags
        html = self.LINK_PATTERN.sub("", html)
        
        # Remove base64 images
        html = self.BASE64_IMG_PATTERN.sub("", html)
        
        # Replace SVG content with placeholder
        html = self.SVG_PATTERN.sub(
            r"\1[SVG Image]\3",
            html
        )
        
        # Normalize whitespace
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'\n+', '\n', html)
        
        return html.strip()
    
    async def html_to_markdown(self, html: str, max_tokens: int = 32768) -> str:
        """
        Convert HTML to clean Markdown using ReaderLM-v2.
        
        Args:
            html: Raw HTML content
            max_tokens: Maximum context length
            
        Returns:
            Clean Markdown text
        """
        # Clean HTML first
        cleaned_html = self.clean_html(html)
        
        # Truncate if too long
        if len(cleaned_html) > max_tokens * 4:  # Rough char-to-token ratio
            logger.warning(f"HTML too long ({len(cleaned_html)} chars), truncating")
            cleaned_html = cleaned_html[:max_tokens * 4]
        
        # Create prompt for ReaderLM-v2
        prompt = f"""Convert the following HTML to clean, well-formatted Markdown. Preserve structure and content accuracy.

HTML:
{cleaned_html}

Markdown:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that converts HTML to clean Markdown format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=16384,
            )
            
            markdown = response.choices[0].message.content
            logger.debug(f"Converted HTML to Markdown ({len(markdown)} chars)")
            
            return markdown
            
        except Exception as e:
            logger.error(f"Error converting HTML to Markdown: {e}")
            # Fallback: return cleaned HTML
            return cleaned_html
    
    async def extract_facts(
        self,
        content: str,
        source_url: str,
        max_facts: int = 20
    ) -> List[Dict[str, str]]:
        """
        Extract structured facts from content.
        
        Args:
            content: Markdown or text content
            source_url: Source URL for attribution
            max_facts: Maximum number of facts to extract
            
        Returns:
            List of fact dictionaries with 'fact' and 'source' fields
        """
        prompt = f"""Extract key facts and information from the following content. Return a JSON array of facts.

Each fact should be:
- Concise and specific
- Factually accurate
- Self-contained
- Relevant and important

Content:
{content[:8000]}  # Limit context

Return only a JSON array in this format:
[
  {{"fact": "fact statement 1", "category": "category1"}},
  {{"fact": "fact statement 2", "category": "category2"}}
]

Extract up to {max_facts} facts."""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts structured facts from content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=4096,
            )
            
            facts_json = response.choices[0].message.content
            
            # Parse JSON
            import json
            facts = json.loads(facts_json)
            
            # Add source URL
            for fact in facts:
                fact["source"] = source_url
            
            logger.info(f"Extracted {len(facts)} facts from {source_url}")
            
            return facts
            
        except Exception as e:
            logger.error(f"Error extracting facts: {e}")
            return []
    
    async def extract_structured_data(
        self,
        html: str,
        schema: Dict,
    ) -> Optional[Dict]:
        """
        Extract structured data using a JSON schema.
        
        Args:
            html: Raw HTML content
            schema: JSON schema defining the structure
            
        Returns:
            Extracted structured data matching schema
        """
        cleaned_html = self.clean_html(html)
        
        prompt = f"""Extract structured data from the following HTML according to the provided JSON schema.

JSON Schema:
{json.dumps(schema, indent=2)}

HTML:
{cleaned_html[:8000]}

Return only valid JSON matching the schema:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts structured data from HTML."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=4096,
            )
            
            data_json = response.choices[0].message.content
            
            # Parse JSON
            import json
            data = json.loads(data_json)
            
            logger.info("Extracted structured data")
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            return None


# Add json import at top
import json
