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
# LaunchAgents call srv by its real path, so they keep working if the /usr/local/bin link goes stale
SRV_BIN = SETUP_DIR / "bin" / "srv"

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


def install_agent(name, args, trigger):
    """(Re)load LaunchAgent com.homeserver.<name> running `srv <args>`; trigger is plist XML (when to run)."""
    label = f"com.homeserver.{name}"
    plist = Path.home() / "Library/LaunchAgents" / f"{label}.plist"
    log = Path.home() / "Library/Logs" / f"{name}.log"
    plist.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    argv = "".join(f"<string>{a}</string>" for a in [SRV_BIN, *args])
    plist.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{label}</string>
  <key>ProgramArguments</key>
  <array>{argv}</array>
  {trigger}
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>{Path.home()}/.orbstack/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
  <key>StandardOutPath</key><string>{log}</string>
  <key>StandardErrorPath</key><string>{log}</string>
</dict>
</plist>
""")
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(plist)], capture_output=True)
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist)], check=True)
    ok(f"{label} (log: ~/Library/Logs/{name}.log)")


def daily_at(hour):
    return f"<key>StartCalendarInterval</key><dict><key>Hour</key><integer>{hour}</integer><key>Minute</key><integer>0</integer></dict>"


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
