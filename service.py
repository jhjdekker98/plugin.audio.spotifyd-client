import xbmcaddon
import subprocess, os

addon = xbmcaddon.Addon()
addonName = addon.getAddonInfo('name')
addonPath = addon.getAddonInfo('path')
spotifyPath = addonPath + 'resources/lib/spotifyd/spotifyd'

def getAddonPath():
    return addonPath

def startUp():
    f = open(f"{addonPath}songs.log", "w")
    f.truncate()
    subprocess.Popen([f'{spotifyPath} --no-daemon --config-path {addonPath}resources/spotifyd.conf'], shell=True, stdout=f)

def shutDown():
    subprocess.run(["kill", "$(ps | grep spotify | awk '{print $1}')"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def restart():
    shutDown()
    startUp()

#Check if already running
output = os.popen("ps | grep spotify | grep -v grep").read()
if output.count("\n") == 0:
    startUp()