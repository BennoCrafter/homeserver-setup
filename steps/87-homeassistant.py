#!/usr/bin/env python3
# desc: Home Assistant OS VM in UTM: create it once, start it at login
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import SETUP_DIR, install_agent, ok, step  # noqa: E402

HA_VM = SETUP_DIR / "bin" / "ha-vm"

step("Home Assistant VM")
# Creation must happen in the GUI session (UTM refuses SSH); `ha-vm create` skips an existing VM.
# macOS asks once on the Mac's screen to allow controlling UTM.
install_agent("ha-vm-create", [HA_VM, "create"], "<key>RunAtLoad</key><true/>")
install_agent("ha-vm", [HA_VM, "start"], "<key>RunAtLoad</key><true/>")
ok("VM starts at login; dongle is attached after boot")
