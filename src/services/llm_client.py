import logging
import os
from pydantic import BaseModel
import litellm

# Set environment variables
os.environ["OPENAI_API_KEY"] = "2d58d17283459d2040699cd26696122f5c85a3a0053cf935e116d154af64eb79"
os.environ["OPENAI_BASE_URL"] = "https://dummy.dev51.cbf.dev.paypalinc.com/cosmosai/llm/v1"

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
        model="gpt-4.1",
        temperature=0.0,
        max_tokens=1024,
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get(
            "OPENAI_BASE_URL",
            "https://aiplatform.dev51.cbf.dev.paypalinc.com/cosmosai/llm/v1"
        ),
    )


class LLMClient:
    def __init__(self, config: LLMConfig = None):
        self.config = config or get_llm_config()
        # Configure litellm with custom base URL
        litellm.api_base = self.config.base_url
        litellm.api_key = self.config.api_key

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
