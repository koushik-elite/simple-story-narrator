import logging
import os
from typing import Dict, List
from models.story import ConversationTurn
from pydantic import BaseModel
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llm_client")


class LLMConfig(BaseModel):
    model: str
    temperature: float
    max_tokens: int
    api_key: str
    base_url: str


def get_llm_config() -> LLMConfig:
    return LLMConfig(
        model="gpt-5-nano",
        temperature=1,
        max_tokens=10024,
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", ""),
    )


class LLMClient:
    def __init__(self, config: LLMConfig = None):
        self.config = config or get_llm_config()
        # Configure litellm with custom base URL
        litellm.api_base = self.config.base_url
        litellm.api_key = self.config.api_key
        print(self.config.base_url)

    def call_llm(self, prompt: str) -> str:
        """Call the LLM with the given prompt and return the response."""
        try:
            response = litellm.completion(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return "Error generating response."

    def execute_character_dialogue(self, messages: List[Dict[str, str]]) -> ConversationTurn:
        """Generate a character's dialogue based on their name and input dialogue."""
        try:
            response = litellm.completion(
                model=self.config.model,
                messages=messages,
                messages_format="pydantic",

                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                response_format=ConversationTurn,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return "Error generating response."
