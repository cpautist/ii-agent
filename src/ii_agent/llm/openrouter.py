import os
import openai
from ii_agent.llm.openai import OpenAIDirectClient


class OpenRouterClient(OpenAIDirectClient):
    """LLM client for OpenRouter (OpenAI-compatible API)."""

    def __init__(self, model_name: str, max_retries: int = 2, cot_model: bool = True):
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        headers = {
            "HTTP-Referer": os.getenv(
                "OPENROUTER_HTTP_REFERER",
                "https://github.com/IntelligentAgent/ii-agent",
            ),
            "X-Title": os.getenv("OPENROUTER_X_TITLE", "ii-agent"),
        }
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
            default_headers=headers,
        )
        self.model_name = model_name
        self.max_retries = max_retries
        self.cot_model = cot_model
