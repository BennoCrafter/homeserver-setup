#!/usr/bin/env python3
# desc: Install Homebrew
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import ensure_sudo, ok, step  # noqa: E402

step("Homebrew")

if not shutil.which("brew"):
    ensure_sudo()
    subprocess.run(
        'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL '
        'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        shell=True, check=True)
    zprofile = Path.home() / ".zprofile"
    if not zprofile.exists() or "brew shellenv" not in zprofile.read_text():
        brew = shutil.which("brew") or "/opt/homebrew/bin/brew"
        with zprofile.open("a") as f:
            f.write(f'eval "$({brew} shellenv)"\n')

version = subprocess.run(["brew", "--version"], capture_output=True, text=True, check=True)
ok(f"Homebrew {version.stdout.splitlines()[0].split()[1]}")
