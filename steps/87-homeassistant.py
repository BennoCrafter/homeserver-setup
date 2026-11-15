#!/usr/bin/env python3
# desc: Home Assistant OS VM in UTM (create once, start at login) + Zigbee dongle over TCP
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
install_agent("zigbee-bridge", [SETUP_DIR / "bin" / "zigbee-bridge"], "<key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>ThrottleInterval</key><integer>5</integer>")
ok("VM starts at login; Zigbee dongle served on tcp port 6638")
