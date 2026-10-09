#!/usr/bin/env python3
# desc: Check auto-login / FileVault and print a summary
import getpass
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import APPS_DIR, DATA_DIR, SRV_ROOT, docker_ready, ok, step, warn  # noqa: E402

step("Checks")
user = getpass.getuser()


def run(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout.strip()


if "On" in run("fdesetup", "status"):
    warn("FileVault is ON: after a power cut the Mac waits for a password and no apps start.")
    warn("Turn it off: System Settings > Privacy & Security > FileVault.")

if run("defaults", "read", "/Library/Preferences/com.apple.loginwindow", "autoLoginUser") != user:
    warn("Automatic login is off. OrbStack runs in your user session, so enable:")
    warn(f"System Settings > Users & Groups > Automatically log in as: {user}")
else:
    ok(f"Automatic login enabled for {user}")

if docker_ready():
    ok("Docker engine running")
else:
    warn("Docker engine not running")

ip = run("ipconfig", "getifaddr", "en0") or run("ipconfig", "getifaddr", "en1") or "<ip>"
host = run("scutil", "--get", "LocalHostName") or run("hostname")

print(f"""
  Root   : {SRV_ROOT}
  Apps   : {APPS_DIR}/<app>/compose.yml
  Data   : {DATA_DIR}/<app>/
  Address: {ip}  /  {host}.local
  SSH    : ssh {user}@{host}.local
""")
