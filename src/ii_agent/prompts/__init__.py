from pathlib import Path
from datetime import datetime
import platform

from .system_prompt import SYSTEM_PROMPT, SYSTEM_PROMPT_WITH_SEQ_THINKING
from .gaia_system_prompt import GAIA_SYSTEM_PROMPT

# Load Gemini-specific system prompt
_gemini_path = Path(__file__).with_name("system").joinpath("gemini.txt")
GEMINI_PROMPT = eval(f"f'''{_gemini_path.read_text()}'''")

__all__ = [
    "SYSTEM_PROMPT",
    "SYSTEM_PROMPT_WITH_SEQ_THINKING",
    "GAIA_SYSTEM_PROMPT",
    "GEMINI_PROMPT",
]
