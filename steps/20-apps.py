#!/usr/bin/env python3
# desc: Install apps (Homebrew casks/formulas) and start OrbStack at login
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import BREW_FORMULAS, CASK_APPS, ok, step, warn, wait_docker  # noqa: E402

step("Apps")

for app in BREW_FORMULAS:
    subprocess.run(["brew", "install", app], check=True)
    ok(f"{app} installed")

for app in CASK_APPS:
    subprocess.run(["brew", "install", "--cask", app], check=True)
    ok(f"{app} installed")

if "orbstack" in CASK_APPS:
    subprocess.run(["open", "-ga", "OrbStack"], capture_output=True)
    print("Waiting for the Docker engine (finish the OrbStack onboarding window if it appears)...")
    if wait_docker(300):
        v = subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"],
                            capture_output=True, text=True).stdout.strip()
        ok(f"Docker engine running ({v})")
    else:
        warn("Docker engine not ready. Finish OrbStack's first-run setup, then: ./setup.py apps")

    if shutil.which("orb") and subprocess.run(
            ["orb", "config", "set", "app.start_at_login", "true"], capture_output=True).returncode == 0:
        ok("OrbStack starts at login")
    elif subprocess.run(
            ["osascript", "-e",
             'tell application "System Events" to if not (exists login item "OrbStack") '
             'then make login item at end with properties {path:"/Applications/OrbStack.app", hidden:true}'],
            capture_output=True).returncode == 0:
        ok("OrbStack added to Login Items")
    else:
        warn("Enable 'Start at login' manually in OrbStack > Settings.")
