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
}

__all__ = ["MODEL_TOOL_DEFAULTS"]
