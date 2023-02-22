import os, subprocess

addonPath = os.path.dirname(os.path.realpath(__file__))

fstd = open(f"/tmp/spotifyd-client/songs.log", "w")
ferr = open(f"/tmp/spotifyd-client/error.log", "w")
subprocess.Popen([f"{addonPath}/resources/lib/spotifyd/spotifyd --no-daemon --config-path {addonPath}/resources/spotifyd.conf"])
