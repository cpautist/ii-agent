import os
from ii_agent.llm.openai import OpenAIDirectClient
import openai


class OpenRouterClient(OpenAIDirectClient):
    """Use OpenRouter models via OpenAI-compatible API."""

    def __init__(self, model_name: str, max_retries: int = 2, cot_model: bool = True, provider_options: dict | None = None):
        # Call super to set up basic attributes including self.provider_options
        super().__init__(model_name=model_name, max_retries=max_retries, cot_model=cot_model, provider_options=provider_options)

        # OpenRouter specific client initialization
        # Potentially use api_key and base_url from self.provider_options if not in env
        api_key = os.getenv("OPENROUTER_API_KEY") or self.provider_options.get("openrouter_api_key") or "EMPTY"
        base_url = os.getenv("OPENROUTER_BASE_URL") or self.provider_options.get("openrouter_base_url") or "https://openrouter.ai/api/v1"

        default_headers = {
            "HTTP-Referer": "https://github.com/Intelligent-Internet/ii-agent", # Example, consider making configurable
            "X-Title": "II Agent", # Example, consider making configurable
        }
        # Allow overriding default_headers via provider_options
        if "default_headers" in self.provider_options:
            default_headers.update(self.provider_options["default_headers"])

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            max_retries=1, # Max retries for individual calls, overall retries handled by self.max_retries in generate
            default_headers=default_headers,
        )
        # self.model_name, self.max_retries, self.cot_model are set by super().__init__

