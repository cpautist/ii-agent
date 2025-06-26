
from ii_agent.core.config.model_tool_map import MODEL_TOOL_DEFAULTS

AVAILABLE_MODELS = [
    "anthropic/claude-sonnet-4",
    "google/gemini-2.5-flash-preview-05-20",
    "deepseek/deepseek-chat-v3-0324:free",
    "deepseek/deepseek-chat-v3-0324",
    "google/gemini-2.5-pro-preview",
    "deepseek/deepseek-r1-0528:free",
    "deepseek/deepseek-r1-0528",
    "openai/gpt-4.1",
    "openai/gpt-4.1-mini",
    "openai/gpt-4.1-nano",
    "openai/o4-mini",
    "openai/o4-mini-high",
    "openai/o3",
    "meta-llama/llama-4-maverick",
    "meta-llama/llama-4-maverick:free",
    "google/gemini-2.5-flash-lite-preview-06-17",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-flash-preview-05-20:thinking",
    "x-ai/grok-3-mini-beta",
    "x-ai/grok-3-mini",
    "anthropic/claude-opus-4",
    "google/gemini-2.0-flash-001",
    "google/gemini-2.5-pro",
    "deepseek/deepseek-r1:free",
    "x-ai/grok-3-beta",
]


def test_model_defaults_lookup():
    for model in AVAILABLE_MODELS:
        if model in MODEL_TOOL_DEFAULTS:
            assert isinstance(MODEL_TOOL_DEFAULTS[model], dict)
        else:
            assert MODEL_TOOL_DEFAULTS.get(model, {}) == {}
