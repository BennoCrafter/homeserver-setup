#!/usr/bin/env python3
# desc: Link the 'srv' command into /usr/local/bin
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import BIN_DIR, SETUP_DIR, ensure_sudo, ok, step  # noqa: E402

step("'srv' command")
ensure_sudo()

executables = [SETUP_DIR / "bin" / "srv", SETUP_DIR / "setup.py", *(SETUP_DIR / "steps").glob("*.py")]
for f in executables:
    f.chmod(f.stat().st_mode | 0o111)

subprocess.run(["sudo", "mkdir", "-p", str(BIN_DIR)], check=True)
subprocess.run(["sudo", "ln", "-sfn", str(SETUP_DIR / "bin" / "srv"), str(BIN_DIR / "srv")], check=True)
ok(f"{BIN_DIR / 'srv'} -> {SETUP_DIR / 'bin' / 'srv'} (edits to bin/srv apply immediately)")
