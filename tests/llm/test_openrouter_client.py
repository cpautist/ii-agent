import pytest
from ii_agent.llm.openrouter import OpenRouterClient


def test_openrouter_client_init(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://example.com")
    client = OpenRouterClient(model_name="openai/o4-mini")
    assert client.model_name == "openai/o4-mini"
    assert client.client.base_url == "https://example.com"
