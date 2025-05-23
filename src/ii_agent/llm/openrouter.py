import os
from ii_agent.llm.openai import OpenAIDirectClient
import openai


class OpenRouterClient(OpenAIDirectClient):
    """Use OpenRouter models via OpenAI-compatible API."""

    def __init__(self, model_name: str, max_retries: int = 2, cot_model: bool = True):
        api_key = os.getenv("OPENROUTER_API_KEY", "EMPTY")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        default_headers = {
            "HTTP-Referer": "https://github.com/Intelligent-Internet/ii-agent",
            "X-Title": "II Agent",
        }
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            max_retries=1,
            default_headers=default_headers,
        )
        self.model_name = model_name
        self.max_retries = max_retries
        self.cot_model = cot_model

