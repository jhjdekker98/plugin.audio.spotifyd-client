import xbmc, xbmcaddon
import subprocess, os

addon = xbmcaddon.Addon()
addonName = addon.getAddonInfo('name')
addonPath = addon.getAddonInfo('path')
spotifyPath = addonPath + 'resources/lib/spotifyd/spotifyd'

def getAddonPath():
    return addonPath

def startUp():
    if not os.path.exists("/tmp/spotifyd-client"):
        os.makedirs("/tmp/spotifyd-client")
    fstd = open("/tmp/spotifyd-client/songs.log", "w")
    ferr = open("/tmp/spotifyd-client/error.log", "w")
    subprocess.Popen([f"{addonPath}/resources/lib/spotifyd/spotifyd --no-daemon --config-path {addonPath}/resources/spotifyd.conf"], stdout=fstd, stderr=ferr)

def shutDown():
    subprocess.run(["kill", "$(ps | grep spotify | awk '{print $1}')"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def restart():
    shutDown()
    startUp()

#Check if already running
output = os.popen("ps | grep spotify | grep -v grep").read()
if output.count("\n") == 0:
    startUp()
