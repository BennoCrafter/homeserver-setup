SRV_ROOT = "/Users/homeserver/srv"  # apps/, data/ and setup/ live here
SERVER_NAME = "homeserver"  # hostname -> homeserver.local (empty = don't change)
TZ = "Europe/Berlin"  # passed to every app as TZ
DISPLAY_SLEEP_MIN = 15  # display sleep in minutes (the system itself never sleeps)
CASK_APPS = "orbstack tailscale"  # Homebrew casks to install, space-separated (keep orbstack: it provides Docker)
