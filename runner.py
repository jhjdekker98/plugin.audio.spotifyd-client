import xbmcaddon
import subprocess

addonPath = xbmcaddon.Addon().getAddonInfo('path')

fstd = open(f"/tmp/spotifyd-client/songs.log", "w")
ferr = open(f"/tmp/spotifyd-client/error.log", "w")
subprocess.Popen([f"{addonPath}/resources/lib/spotifyd/spotifyd --no-daemon --config-path {addonPath}/resources/spotifyd.conf"])
