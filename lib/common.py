"""Shared helpers, imported by setup.py and every step. macOS only."""
import os
import platform
import subprocess
import sys
import threading
import time
from pathlib import Path

SETUP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SETUP_DIR))
import config  # noqa: E402

SRV_ROOT = Path(getattr(config, "SRV_ROOT", "~/srv")).expanduser()
SERVER_NAME = getattr(config, "SERVER_NAME", "")
TZ = getattr(config, "TZ", "Europe/Berlin")
DISPLAY_SLEEP_MIN = getattr(config, "DISPLAY_SLEEP_MIN", 15)
CASK_APPS = getattr(config, "CASK_APPS", "orbstack").split()
BREW_FORMULAS = getattr(config, "BREW_FORMULAS", "").split()

APPS_DIR = SRV_ROOT / "apps"
DATA_DIR = SRV_ROOT / "data"
BIN_DIR = Path("/usr/local/bin")
AGENT_LABEL = "com.homeserver.srv-up"
AGENT_PLIST = Path.home() / "Library/LaunchAgents" / f"{AGENT_LABEL}.plist"

os.environ["PATH"] = f"{Path.home()}/.orbstack/bin:/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")

BLUE, YEL, RED, GRN, OFF = "\033[1;34m", "\033[1;33m", "\033[1;31m", "\033[1;32m", "\033[0m"


def step(msg):
    print(f"\n{BLUE}==>{OFF} {msg}")


def ok(msg):
    print(f"{GRN}  ✓{OFF} {msg}")


def warn(msg):
    print(f"{YEL}  ! {msg}{OFF}")


def die(msg):
    print(f"{RED}[error]{OFF} {msg}", file=sys.stderr)
    sys.exit(1)


if platform.system() != "Darwin":
    die("This is for macOS only.")
if os.geteuid() == 0:
    die("Run as your normal user (not with sudo). You'll be asked for your password when needed.")

_sudo_keepalive_started = False


def ensure_sudo():
    """Ask for the password once; a background thread keeps sudo alive for all steps."""
    global _sudo_keepalive_started
    subprocess.run(["sudo", "-v"], check=True)
    if _sudo_keepalive_started:
        return

    def keepalive():
        while True:
            time.sleep(50)
            if subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode != 0:
                return

    threading.Thread(target=keepalive, daemon=True).start()
    _sudo_keepalive_started = True


def docker_ready():
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


def wait_docker(seconds=300):
    for i in range(seconds // 2):
        if docker_ready():
            return True
        if i == 0:
            subprocess.run(["open", "-ga", "OrbStack"], capture_output=True)
        time.sleep(2)
    return False
