import types
from unittest.mock import MagicMock

from openai._types import NOT_GIVEN as OpenAI_NOT_GIVEN

from ii_agent.llm.openrouter import OpenRouterClient
from ii_agent.llm.token_counter import TokenCounter
from ii_agent.llm.base import TextPrompt


def make_response(content="hi"):
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content, tool_calls=None))],
        usage=types.SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )


def test_force_tool_default_true(monkeypatch):
    client = OpenRouterClient(model_name="test")
    monkeypatch.setattr(TokenCounter, "count_tokens", lambda self, msgs: 100)
    mock_api = MagicMock()
    mock_api.chat.completions.create.return_value = make_response()
    client.client = mock_api

    messages = [[TextPrompt(text="hello")]]

    client.generate(messages=messages, max_tokens=5, tool_args={"deep_research": True})

    kwargs = mock_api.chat.completions.create.call_args.kwargs
    assert kwargs["tool_choice"] == "required"


def test_force_tool_disabled(monkeypatch):
    client = OpenRouterClient(model_name="test")
    monkeypatch.setattr(TokenCounter, "count_tokens", lambda self, msgs: 100)
    mock_api = MagicMock()
    mock_api.chat.completions.create.return_value = make_response()
    client.client = mock_api

    messages = [[TextPrompt(text="hello")]]

    client.generate(
        messages=messages,
        max_tokens=5,
        tool_args={"deep_research": True, "force_tool": False},
    )

    kwargs = mock_api.chat.completions.create.call_args.kwargs
    assert kwargs["tool_choice"] is OpenAI_NOT_GIVEN
