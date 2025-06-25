import sys
from pathlib import Path

# Add the repository's src directory to PYTHONPATH so local modules are importable
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if SRC_PATH.exists():
    sys.path.insert(0, str(SRC_PATH))

# Provide a minimal "anthropic" stub so tests can run without the package
if "anthropic" not in sys.modules:
    import types

    anthropic_stub = types.ModuleType("anthropic")
    anthropic_stub.NOT_GIVEN = None
    anthropic_stub.APIConnectionError = Exception
    anthropic_stub.InternalServerError = Exception
    anthropic_stub.RateLimitError = Exception
    anthropic_stub.Anthropic = object
    anthropic_stub.AnthropicVertex = object

    exceptions_stub = types.ModuleType("anthropic._exceptions")
    exceptions_stub.OverloadedError = Exception

    types_stub = types.ModuleType("anthropic.types")
    types_stub.TextBlock = object
    types_stub.ThinkingBlock = type("ThinkingBlock", (), {})
    types_stub.RedactedThinkingBlock = type("RedactedThinkingBlock", (), {})
    types_stub.ImageBlockParam = object
    types_stub.ToolParam = object
    types_stub.ToolResultBlockParam = object
    types_stub.ToolUseBlock = object

    message_params_stub = types.ModuleType(
        "anthropic.types.message_create_params"
    )
    message_params_stub.ToolChoiceToolChoiceAny = object
    message_params_stub.ToolChoiceToolChoiceAuto = object
    message_params_stub.ToolChoiceToolChoiceTool = object

    sys.modules["anthropic"] = anthropic_stub
    sys.modules["anthropic._exceptions"] = exceptions_stub
    sys.modules["anthropic.types"] = types_stub
    sys.modules["anthropic.types.message_create_params"] = message_params_stub

# Provide a minimal "google.genai" stub for Gemini client imports
if "google" not in sys.modules:
    import types
    google_stub = types.ModuleType("google")
    genai_stub = types.ModuleType("google.genai")
    genai_stub.types = types.ModuleType("google.genai.types")
    genai_stub.errors = types.ModuleType("google.genai.errors")
    google_stub.genai = genai_stub
    sys.modules["google"] = google_stub
    sys.modules["google.genai"] = genai_stub
    sys.modules["google.genai.types"] = genai_stub.types
    sys.modules["google.genai.errors"] = genai_stub.errors

# Ensure llm.base exports ThinkingBlock aliases even if anthropic is stubbed
import ii_agent.llm.base as llm_base
if not hasattr(llm_base, "ThinkingBlock"):
    llm_base.ThinkingBlock = getattr(llm_base, "AnthropicThinkingBlock", object)
if not hasattr(llm_base, "RedactedThinkingBlock"):
    llm_base.RedactedThinkingBlock = getattr(
        llm_base, "AnthropicRedactedThinkingBlock", object
    )
