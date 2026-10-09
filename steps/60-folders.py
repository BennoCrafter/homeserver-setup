#!/usr/bin/env python3
# desc: Create srv/apps and srv/data
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import APPS_DIR, DATA_DIR, ok, step  # noqa: E402

step("Folders")
APPS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
ok(f"Apps: {APPS_DIR}")
ok(f"Data: {DATA_DIR}")
