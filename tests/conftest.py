import sys
from pathlib import Path

# Add the repository's src directory to PYTHONPATH so local modules are importable
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if SRC_PATH.exists():
    sys.path.insert(0, str(SRC_PATH))
