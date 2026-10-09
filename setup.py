#!/usr/bin/env python3
"""Run all setup steps, or only the ones you name.

  ./setup.py                 # everything
  ./setup.py power ssh       # by name
  ./setup.py 30 50           # by number
  ./setup.py --list          # show steps

Every step is also runnable on its own: ./steps/30-power.py
"""

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import GRN, OFF, SETUP_DIR, die, ensure_sudo  # noqa: E402

STEPS_DIR = SETUP_DIR / "steps"
ALL = sorted(STEPS_DIR.glob("[0-9][0-9]-*.py"))


def desc(f):
    m = re.search(r"^# desc: (.*)$", f.read_text(), re.MULTILINE)
    return m.group(1) if m else ""


def find(arg):
    for f in ALL:
        b = f.stem
        if b == arg or b.split("-", 1)[0] == arg or b.split("-", 1)[1] == arg:
            return f
    return None


def main(argv):
    if argv[:1] and argv[0] in ("--list", "-l"):
        for f in ALL:
            print(f"  {f.stem:<16} {desc(f)}")
        return 0

    selected = ALL if not argv else []
    for arg in argv:
        f = find(arg)
        if not f:
            die(f"Unknown step '{arg}'. See ./setup.py --list")
        selected.append(f)

    ensure_sudo()
    for f in selected:
        if subprocess.run([sys.executable, str(f)]).returncode != 0:
            die(f"Step {f.stem} failed")
    print(f"\n{GRN}Done.{OFF}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
