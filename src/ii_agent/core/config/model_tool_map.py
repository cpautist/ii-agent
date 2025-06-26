"""Default tool settings for each model.

The flags defined here are merged with any settings provided by the UI.
"""

from typing import Dict, Any

# Mapping of model names to their default tool settings. Incoming
# tool flags from the UI will override these defaults.
MODEL_TOOL_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "anthropic/claude-sonnet-4": {
        "deep_research": False,
        "pdf": True,
        "media_generation": True,
        "audio_generation": True,
        "browser": True,
    },
    "anthropic/claude-opus-4": {
        "deep_research": False,
        "pdf": True,
        "media_generation": True,
        "audio_generation": True,
        "browser": True,
    },
    "google/gemini-2.5-flash-001": {
        "deep_research": True,
    },
    "google/gemini-2.5-pro": {
        "deep_research": True,
    },
    "openai/gpt-4.1-mini": {
        "deep_research": True,
    },
    "openai/gpt-4.1-nano": {
        "deep_research": True,
    },
}

__all__ = ["MODEL_TOOL_DEFAULTS"]
