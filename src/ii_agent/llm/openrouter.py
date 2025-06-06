import os
from ii_agent.llm.openai import OpenAIDirectClient
import openai


class OpenRouterClient(OpenAIDirectClient):
    """Use OpenRouter models via OpenAI-compatible API.

    This client supports specifying fallback models that will be tried in order
    if the primary model fails. Fallback models can be provided via the
    ``fallback_models`` key in ``provider_options`` or the
    ``OPENROUTER_FALLBACK_MODELS`` environment variable (comma separated).
    """

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

        # Determine fallback models
        fallback_env = os.getenv("OPENROUTER_FALLBACK_MODELS")
        if fallback_env:
            self.fallback_models = [m.strip() for m in fallback_env.split(",") if m.strip()]
        else:
            self.fallback_models = []

        if "fallback_models" in self.provider_options:
            self.fallback_models.extend(self.provider_options["fallback_models"])  # type: ignore[arg-type]

    def generate(
        self,
        messages,
        max_tokens,
        system_prompt: str | None = None,
        temperature: float = 0.0,
        tools: list = [],
        tool_choice: dict | None = None,
        provider_options: dict | None = None,
    ):
        """Generate with automatic fallback across models."""

        # Combine fallback models from initialization with any provided at call time
        call_fallbacks = []
        if provider_options and "fallback_models" in provider_options:
            call_fallbacks = provider_options["fallback_models"]

        models_to_try = [self.model_name] + call_fallbacks + self.fallback_models

        last_err: Exception | None = None
        original_model = self.model_name
        for candidate in models_to_try:
            self.model_name = candidate
            try:
                return super().generate(
                    messages=messages,
                    max_tokens=max_tokens,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    tools=tools,
                    tool_choice=tool_choice,
                    provider_options=provider_options,
                )
            except Exception as e:
                last_err = e
                continue
        self.model_name = original_model
        if last_err is not None:
            raise last_err


