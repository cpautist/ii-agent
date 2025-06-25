import types
from unittest.mock import MagicMock

from ii_agent.llm.openrouter import OpenRouterClient
from ii_agent.llm.base import TextPrompt


def make_response(content="hi"):
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content, tool_calls=None))],
        usage=types.SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )


def test_deep_research_triggers_tool_choice(monkeypatch):
    client = OpenRouterClient(model_name="test")
    monkeypatch.setattr(
        OpenRouterClient, "DEEP_RESEARCH_TOKEN_THRESHOLD", 10, raising=False
    )
    mock_api = MagicMock()
    mock_api.chat.completions.create.return_value = make_response()
    client.client = mock_api

    messages = [[TextPrompt(text="a" * 40)]]

    client.generate(
        messages=messages,
        max_tokens=5,
        tool_args={"deep_research": True},
    )

    kwargs = mock_api.chat.completions.create.call_args.kwargs
    assert kwargs["tool_choice"] == "required"
    assert kwargs["extra_body"]["parallel_tool_calls"] is False
