#!/usr/bin/env python3
# desc: Enable SSH (Remote Login)
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import ensure_sudo, ok, step, warn  # noqa: E402

step("SSH (Remote Login)")


def ssh_on():
    try:
        with socket.create_connection(("localhost", 22), timeout=1):
            return True
    except OSError:
        return False


if ssh_on():
    ok("SSH already enabled")
    sys.exit(0)

ensure_sudo()
subprocess.run(["sudo", "systemsetup", "-setremotelogin", "on"], capture_output=True)
if not ssh_on():
    subprocess.run(["sudo", "launchctl", "enable", "system/com.openssh.sshd"], capture_output=True)
    subprocess.run(["sudo", "launchctl", "bootstrap", "system",
                     "/System/Library/LaunchDaemons/ssh.plist"], capture_output=True)
    time.sleep(1)

if ssh_on():
    ok("SSH enabled")
else:
    warn("macOS blocked this (Terminal needs Full Disk Access).")
    warn("Enable manually: System Settings > General > Sharing > Remote Login.")
