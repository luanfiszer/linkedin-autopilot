import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT / "scripts", ROOT / ".claude" / "skills" / "li-human"):
    sys.path.insert(0, str(p))
