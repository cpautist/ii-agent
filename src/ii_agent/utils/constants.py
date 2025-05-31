UPLOAD_FOLDER_NAME = "uploaded_files"
COMPLETE_MESSAGE = "Completed the task."
DEFAULT_MODEL = "deepseek/deepseek-r1-0528:free" # Make sure this is a key in MODEL_CAPABILITIES

# MODEL_CAPABILITIES
# Defines properties for various models, including their provider,
# tool support, and context window size.
#
# - provider: Identifier for the LLM client (e.g., 'openrouter-direct', 'anthropic-direct').
# - supports_tools: Boolean indicating if the model supports tool usage.
# - context_window: Integer representing the model's context window size in tokens.
#                   (Note: These are approximate values and might vary or change.)
# - description: Optional string for a brief model description.
MODEL_CAPABILITIES = {
    # --- Anthropic Direct Models (Example) ---
    # "claude-3-opus-20240229": { # Example if directly using Anthropic
    #     "provider": "anthropic-direct",
    #     "supports_tools": True,
    #     "context_window": 200000,
    #     "description": "Anthropic's most powerful model."
    # },
    # "claude-3.5-sonnet-20240620": { # Example for direct Anthropic
    # "provider": "anthropic-direct",
    # "supports_tools": True,
    # "context_window": 200000,
    # "description": "Anthropic's Claude 3.5 Sonnet model."
    # },


    # --- OpenAI Direct Models (Examples) ---
    "gpt-4o": {
        "provider": "openai-direct",
        "supports_tools": True,
        "context_window": 128000,
        "description": "OpenAI's GPT-4 Omni model."
    },
    "gpt-4o-mini": {
        "provider": "openai-direct",
        "supports_tools": True,
        "context_window": 128000, # Assuming same as gpt-4o, verify
        "description": "OpenAI's GPT-4 Omni Mini model."
    },
    "gpt-4-turbo": {
        "provider": "openai-direct",
        "supports_tools": True,
        "context_window": 128000,
        "description": "OpenAI's GPT-4 Turbo model."
    },
    "gpt-4-turbo-preview": { # Often an alias for a recent gpt-4-turbo snapshot
        "provider": "openai-direct",
        "supports_tools": True,
        "context_window": 128000,
        "description": "OpenAI's GPT-4 Turbo Preview model."
    },
    "gpt-4.1-2025-04-14": { # Hypothetical future model names from old map
        "provider": "openai-direct", "supports_tools": True, "context_window": 128000
    },
    "o4-mini-2025-04-16": { # Hypothetical future model names from old map
        "provider": "openai-direct", "supports_tools": True, "context_window": 128000
    },
    "o3-2025-04-16": { # Hypothetical future model names from old map - gpt-3.5 based
        "provider": "openai-direct", "supports_tools": True, "context_window": 16385
    },
    "gpt-4.1-mini-2025-04-14": { # Hypothetical future model names from old map
        "provider": "openai-direct", "supports_tools": True, "context_window": 128000
    },
    "gpt-4.1-nano-2025-04-14": { # Hypothetical future model names from old map
        "provider": "openai-direct", "supports_tools": True, "context_window": 32000 # Educated guess for a "nano"
    },
    "o3-mini-2025-01-31": { # Hypothetical future model names from old map - gpt-3.5 based
        "provider": "openai-direct", "supports_tools": True, "context_window": 16385
    },
    "chatgpt-4o-latest": { # Alias for gpt-4o
        "provider": "openai-direct", "supports_tools": True, "context_window": 128000
    },

    # --- OpenRouter Proxied Models (Derived from old MODEL_TO_PROVIDER_MAP) ---
    "deepseek/deepseek-r1-0528:free": { # DEFAULT_MODEL
        "provider": "openrouter-direct",
        "supports_tools": True,
        "context_window": 128000, # Assumption for R1 series
        "description": "Deepseek R1 0528 (Free on OpenRouter)"
    },
    "deepseek/deepseek-r1-0528": {
        "provider": "openrouter-direct",
        "supports_tools": True,
        "context_window": 128000,
        "description": "Deepseek R1 0528 (Paid on OpenRouter)"
    },
    "openai/o4-mini-high": { # GPT-4o Mini equivalent
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "qwen/qwen3-30b-a3b:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 65536 # Qwen models vary, 32k-128k+
    },
    "qwen/qwen3-235b-a22b:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 65536
    },
    "tngtech/deepseek-r1t-chimera:free": { # Chimera likely tool-supporting Deepseek variant
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "anthropic/claude-3.7-sonnet:thinking": { # Special version with thinking
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 200000
    },
    "deepseek/deepseek-r1": { # Generic R1
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "openai/gpt-4.1": { # Older GPT-4 variant
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "openai/o3": { # GPT-3.5 Turbo
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 16385
    },
    "openai/o4-mini": { # GPT-4o Mini
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "openai/gpt-4.1-mini": { # Older GPT-4 Mini variant
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "openai/gpt-4.1-nano": { # Older GPT-4 Nano variant
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 32000 # Educated guess
    },
    "x-ai/grok-3-mini-beta": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000 # Grok models are large
    },
    "x-ai/grok-3-beta": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "meta-llama/llama-4-maverick:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000 # Llama 4 likely large
    },
    "meta-llama/llama-4-maverick": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "meta-llama/llama-4-scout:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "deepseek/deepseek-v3-base:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000 # V3 likely large
    },
    "google/gemini-2.5-pro-exp-03-25": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 1000000 # Gemini 1.5/2.5 have very large context windows
    },
    "deepseek/deepseek-chat-v3-0324:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "deepseek/deepseek-chat-v3-0324": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "deepseek/deepseek-r1-zero:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "anthropic/claude-3.7-sonnet:beta": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 200000
    },
    "openai/o3-mini-high": { # GPT-3.5 Turbo Mini (higher quality variant)
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 16385
    },
    "openai/o3-mini": { # GPT-3.5 Turbo Mini
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 16385 # Or 4k/8k if older variant
    },
    "deepseek/deepseek-r1-distill-llama-70b:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 32768 # Distilled models might have smaller context
    },
    "deepseek/deepseek-r1:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "deepseek/deepseek-chat:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 32768 # General chat models might vary
    },
    "google/gemini-2.0-flash-exp:free": { # Gemini Flash
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 1000000 # Flash also has large context
    },
    "openai/gpt-4o-2024-11-20": { # Future dated GPT-4o
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 128000
    },
    "qwen/qwen-2.5-coder-32b-instruct:free": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 65536 # Qwen Coder
    },
    "anthropic/claude-3.5-haiku-20241022:beta": { # Haiku
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 200000
    },
    "meta-llama/Meta-Llama-3.1-70B-Instruct": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 131072 # Llama 3.1 uses 128k
    },
    "meta-llama/llama-3.1-8b-instruct": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 131072
    },
    "mistralai/Mixtral-8x22B-Instruct-v0.1": {
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 65536 # Or 128k, Mixtral varies
    },
    "google/palm-2": { # Older PaLM-2
        "provider": "openrouter-direct", "supports_tools": False, "context_window": 8192
    },
    "anthropic/claude-opus-4": { # Likely Claude 3 Opus
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 200000
    },
    "anthropic/claude-sonnet-4": { # Likely Claude 3.5 Sonnet or Claude 3 Sonnet
        "provider": "openrouter-direct", "supports_tools": True, "context_window": 200000
    }
}
