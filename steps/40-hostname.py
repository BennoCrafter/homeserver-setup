#!/usr/bin/env python3
# desc: Set hostname from SERVER_NAME in config.py
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import SERVER_NAME, ensure_sudo, ok, step  # noqa: E402

step("Hostname")

if not SERVER_NAME:
    current = subprocess.run(["scutil", "--get", "LocalHostName"],
                              capture_output=True, text=True).stdout.strip()
    ok(f"SERVER_NAME is empty, leaving hostname as {current}")
    sys.exit(0)

ensure_sudo()
for key in ("ComputerName", "HostName", "LocalHostName"):
    subprocess.run(["sudo", "scutil", "--set", key, SERVER_NAME], check=True)
ok(f"Reachable as {SERVER_NAME}.local")
