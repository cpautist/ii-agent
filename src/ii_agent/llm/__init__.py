from ii_agent.llm.base import LLMClient
from ii_agent.llm.openai import OpenAIDirectClient
from ii_agent.llm.anthropic import AnthropicDirectClient
from ii_agent.llm.openrouter import OpenRouterClient


def get_client(client_name: str, provider_options: dict | None = None, **kwargs) -> LLMClient:
    """Get a client for a given client name."""
    if client_name == "anthropic-direct":
        return AnthropicDirectClient(provider_options=provider_options, **kwargs)
    elif client_name == "openai-direct":
        return OpenAIDirectClient(provider_options=provider_options, **kwargs)
    elif client_name == "openrouter-direct":
        return OpenRouterClient(provider_options=provider_options, **kwargs)
    else:
        raise ValueError(f"Unknown client name: {client_name}")


__all__ = [
    "LLMClient",
    "OpenAIDirectClient",
    "AnthropicDirectClient",
    "OpenRouterClient",
    "get_client",
]
