#!/usr/bin/env python3
# desc: LaunchAgent that runs 'srv up' at login
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import SRV_BIN, install_agent, step  # noqa: E402

step("Auto-start apps at login")
install_agent("srv-up", [SRV_BIN, "up"], "<key>RunAtLoad</key><true/>")
