UPLOAD_FOLDER_NAME = "uploaded_files"
COMPLETE_MESSAGE = "Completed the task."
DEFAULT_MODEL = "claude-3-7-sonnet@20250219"

# Mapping of model names to the provider used to serve them. This is used
# to automatically determine the correct LLM backend when only the model
# is specified in ``agent_config.yaml`` or via command line. The values
# correspond to the provider identifiers used in ``parse_common_args``.
MODEL_TO_PROVIDER_MAP = {
    # --- OpenRouter Proxied Models (Examples) ---
    "openai/o4-mini-high": "openrouter",
    "qwen/qwen3-30b-a3b:free": "openrouter",
    "qwen/qwen3-235b-a22b:free": "openrouter",
    "tngtech/deepseek-r1t-chimera:free": "openrouter",
    "anthropic/claude-3.7-sonnet:thinking": "openrouter",
    "deepseek/deepseek-r1": "openrouter",
    "openai/gpt-4.1": "openrouter",
    "openai/o3": "openrouter",
    "openai/o4-mini": "openrouter",
    "openai/gpt-4.1-mini": "openrouter",
    "openai/gpt-4.1-nano": "openrouter",
    "x-ai/grok-3-mini-beta": "openrouter",
    "x-ai/grok-3-beta": "openrouter",
    "meta-llama/llama-4-maverick:free": "openrouter",
    "meta-llama/llama-4-maverick": "openrouter",
    "meta-llama/llama-4-scout:free": "openrouter",
    "deepseek/deepseek-v3-base:free": "openrouter",
    "google/gemini-2.5-pro-exp-03-25": "openrouter",
    "deepseek/deepseek-chat-v3-0324:free": "openrouter",
    "deepseek/deepseek-chat-v3-0324": "openrouter",
    "deepseek/deepseek-r1-zero:free": "openrouter",
    "anthropic/claude-3.7-sonnet:beta": "openrouter",
    "openai/o3-mini-high": "openrouter",
    "openai/o3-mini": "openrouter",
    "deepseek/deepseek-r1-distill-llama-70b:free": "openrouter",
    "deepseek/deepseek-r1:free": "openrouter",
    "deepseek/deepseek-chat:free": "openrouter",
    "google/gemini-2.0-flash-exp:free": "openrouter",
    "openai/gpt-4o-2024-11-20": "openrouter",
    "qwen/qwen-2.5-coder-32b-instruct:free": "openrouter",
    "anthropic/claude-3.5-haiku-20241022:beta": "openrouter",
    "meta-llama/Meta-Llama-3.1-70B-Instruct": "openrouter",
    "meta-llama/llama-3.1-8b-instruct": "openrouter",
    "mistralai/Mixtral-8x22B-Instruct-v0.1": "openrouter",
    "google/palm-2": "openrouter",
    # Additional models requested
    "deepseek/deepseek-r1-0528:free": "openrouter",
    "deepseek/deepseek-r1-0528": "openrouter",
    "anthropic/claude-opus-4": "openrouter",
    "anthropic/claude-sonnet-4": "openrouter",

    # --- Direct OpenAI Models (Examples) ---
    "gpt-4.1-2025-04-14": "openai",
    "o4-mini-2025-04-16": "openai",
    "o3-2025-04-16": "openai",
    "gpt-4.1-mini-2025-04-14": "openai",
    "gpt-4.1-nano-2025-04-14": "openai",
    "o3-mini-2025-01-31": "openai",
    "chatgpt-4o-latest": "openai",
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4-turbo-preview": "openai",
}

