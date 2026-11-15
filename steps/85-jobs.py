#!/usr/bin/env python3
# desc: LaunchAgents for nightly backups, portal update requests and nightly auto-updates
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import DATA_DIR, SRV_BIN, daily_at, install_agent, step  # noqa: E402

step("Background jobs")
requests = DATA_DIR / "portal" / "requests"
requests.mkdir(parents=True, exist_ok=True)
install_agent("srv-backup", [SRV_BIN, "backup"], daily_at(3))
install_agent("srv-auto-update", [SRV_BIN, "auto-update"], daily_at(4))
install_agent("srv-requests", [SRV_BIN, "process-requests"], f"<key>WatchPaths</key><array><string>{requests}</string></array>")
