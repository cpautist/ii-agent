UPLOAD_FOLDER_NAME = "uploaded_files"
COMPLETE_MESSAGE = "Completed the task."
DEFAULT_MODEL = "deepseek/deepseek-r1-0528:free"

# Mapping of model names to the provider used to serve them. This is used
# to automatically determine the correct LLM backend when only the model
# is specified in ``agent_config.yaml`` or via command line. The values
# correspond to the provider identifiers used in ``parse_common_args``.
MODEL_TO_PROVIDER_MAP = {
    # --- OpenRouter Proxied Models (Examples) ---
    "openai/o4-mini-high": "openrouter-direct",
    "qwen/qwen3-30b-a3b:free": "openrouter-direct",
    "qwen/qwen3-235b-a22b:free": "openrouter-direct",
    "tngtech/deepseek-r1t-chimera:free": "openrouter-direct",
    "anthropic/claude-3.7-sonnet:thinking": "openrouter-direct",
    "deepseek/deepseek-r1": "openrouter-direct",
    "openai/gpt-4.1": "openrouter-direct",
    "openai/o3": "openrouter-direct",
    "openai/o4-mini": "openrouter-direct",
    "openai/gpt-4.1-mini": "openrouter-direct",
    "openai/gpt-4.1-nano": "openrouter-direct",
    "x-ai/grok-3-mini-beta": "openrouter-direct",
    "x-ai/grok-3-beta": "openrouter-direct",
    "meta-llama/llama-4-maverick:free": "openrouter-direct",
    "meta-llama/llama-4-maverick": "openrouter-direct",
    "meta-llama/llama-4-scout:free": "openrouter-direct",
    "deepseek/deepseek-v3-base:free": "openrouter-direct",
    "google/gemini-2.5-pro-exp-03-25": "openrouter-direct",
    "deepseek/deepseek-chat-v3-0324:free": "openrouter-direct",
    "deepseek/deepseek-chat-v3-0324": "openrouter-direct",
    "deepseek/deepseek-r1-zero:free": "openrouter-direct",
    "anthropic/claude-3.7-sonnet:beta": "openrouter-direct",
    "openai/o3-mini-high": "openrouter-direct",
    "openai/o3-mini": "openrouter-direct",
    "deepseek/deepseek-r1-distill-llama-70b:free": "openrouter-direct",
    "deepseek/deepseek-r1:free": "openrouter-direct",
    "deepseek/deepseek-chat:free": "openrouter-direct",
    "google/gemini-2.0-flash-exp:free": "openrouter-direct",
    "openai/gpt-4o-2024-11-20": "openrouter-direct",
    "qwen/qwen-2.5-coder-32b-instruct:free": "openrouter-direct",
    "anthropic/claude-3.5-haiku-20241022:beta": "openrouter-direct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct": "openrouter-direct",
    "meta-llama/llama-3.1-8b-instruct": "openrouter-direct",
    "mistralai/Mixtral-8x22B-Instruct-v0.1": "openrouter-direct",
    "google/palm-2": "openrouter-direct",
    # Additional models requested
    "deepseek/deepseek-r1-0528:free": "openrouter-direct",
    "deepseek/deepseek-r1-0528": "openrouter-direct",
    "anthropic/claude-opus-4": "openrouter-direct",
    "anthropic/claude-sonnet-4": "openrouter-direct",
    # --- Direct OpenAI Models (Examples) ---
    "gpt-4.1-2025-04-14": "openai-direct",
    "o4-mini-2025-04-16": "openai-direct",
    "o3-2025-04-16": "openai-direct",
    "gpt-4.1-mini-2025-04-14": "openai-direct",
    "gpt-4.1-nano-2025-04-14": "openai-direct",
    "o3-mini-2025-01-31": "openai-direct",
    "chatgpt-4o-latest": "openai-direct",
    "gpt-4o": "openai-direct",
    "gpt-4o-mini": "openai-direct",
    "gpt-4-turbo": "openai-direct",
    "gpt-4-turbo-preview": "openai-direct",
}
