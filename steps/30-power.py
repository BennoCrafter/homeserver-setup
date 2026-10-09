#!/usr/bin/env python3
# desc: Never sleep, wake-on-LAN, restart after power loss
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import DISPLAY_SLEEP_MIN, ensure_sudo, ok, step  # noqa: E402

step("Power settings")
ensure_sudo()

subprocess.run(["sudo", "pmset", "-a",
                "sleep", "0", "disksleep", "0", "displaysleep", str(DISPLAY_SLEEP_MIN),
                "powernap", "0", "womp", "1", "autorestart", "1", "tcpkeepalive", "1"], check=True)
subprocess.run(["sudo", "systemsetup", "-setrestartfreeze", "on"], capture_output=True)
ok(f"No system sleep, display sleep {DISPLAY_SLEEP_MIN} min, wake-on-LAN, auto-restart after power failure")
