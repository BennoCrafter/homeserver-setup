#!/usr/bin/env python3
# desc: LaunchAgent that runs 'srv up' at login
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import AGENT_LABEL, AGENT_PLIST, BIN_DIR, ok, step  # noqa: E402

step("Auto-start apps at login")

(Path.home() / "Library/LaunchAgents").mkdir(parents=True, exist_ok=True)
(Path.home() / "Library/Logs").mkdir(parents=True, exist_ok=True)

AGENT_PLIST.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{AGENT_LABEL}</string>
  <key>ProgramArguments</key>
  <array><string>{BIN_DIR / "srv"}</string><string>up</string></array>
  <key>RunAtLoad</key><true/>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>{Path.home()}/.orbstack/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
  <key>StandardOutPath</key><string>{Path.home()}/Library/Logs/srv-up.log</string>
  <key>StandardErrorPath</key><string>{Path.home()}/Library/Logs/srv-up.log</string>
</dict>
</plist>
""")

uid = os.getuid()
subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(AGENT_PLIST)], capture_output=True)
subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(AGENT_PLIST)], capture_output=True)
ok("LaunchAgent installed (log: ~/Library/Logs/srv-up.log)")
