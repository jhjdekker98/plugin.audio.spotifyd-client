import xbmcaddon, xbmcgui
import subprocess

addon = xbmcaddon.Addon()
addonName = addon.getAddonInfo('name')
spotifyPath = addon.getAddonInfo('path') + 'resources/lib/spotifyd/spotifyd'

xbmcgui.Dialog().ok(addonName, spotifyPath)
subprocess.run(spotifyPath)
