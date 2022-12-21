import xbmc, xbmcaddon, xbmcgui
import service
import os
import requests, base64, shutil
import threading, _thread
import time
from PIL import Image, ImageFilter

SPOTIFYD_LOG_READ_LINE_AMOUNT = 100
SPOTIFY_API_URL_TOKEN = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL_TRACK = 'https://api.spotify.com/v1/tracks/'
THREAD_LIST_FILE_PATH = '/tmp/runningproc.cfg'
LIGHTNESS_PIXEL_LOCATIONS = [(0.5, 0.5), (0.5, 0.75), (0.35, 0.65), (0.65, 0.65)]

currSong = '<song>'
currArtist = '<artist>'
accessToken = ''
accessTokenExpire = 0

class GUI(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        self.data = kwargs['optional1']

    def onInit(self):
        xbmc.executebuiltin('Container.SetViewMode(50)')

def signatureSuicide(signature):
    lines = []
    if os.path.exists(THREAD_LIST_FILE_PATH):
        # Check signature list
        f = open(THREAD_LIST_FILE_PATH, 'r')
        lines = f.read().splitlines()
        f.close()
    while len(lines) < 2:
        lines.insert(0, '')

    # If LAST signature is OWN signature
    if lines[len(lines)-1] == signature:
        return
    # If second-to-last signature is OWN signature
    if lines[len(lines)-2] == signature:
        #kill self
        #TODO: Remove all occurrences of own signature from file
        _thread.interrupt_main()
        _thread.exit()
    # Write own signature at bottom of list
    f = open(THREAD_LIST_FILE_PATH, 'a')
    f.write(signature + '\n')
    f.close()

def updateTrackData(window):
    accessToken = ''
    accessTokenExpire = 0
    lastTrackId = ''
    signature = base64.b64encode(str(int(time.time())).encode('ascii')).decode('ascii')
    window.setProperty("txtCol", "FF000000")

    while True:
        signatureSuicide(signature)
        trackData = getTrackData(lastTrackId, accessToken, accessTokenExpire)
        if trackData != None:
            accessToken = trackData["accessToken"]
            accessTokenExpire = trackData["accessTokenExpire"]
            images = trackData["json"]["album"]["images"]
            albumArt = updateAlbumArt(lastTrackId, trackData["lastTrackId"], images)
            window.setProperty("txtCol", albumArt["txtCol"])
            window.setProperty("albumArt", albumArt["path"] + ".jpg")
            window.setProperty("albumArtBg", albumArt["path"] + "_b.jpg")
            lastTrackId = trackData["lastTrackId"]
            window.setProperty("currSong", trackData["json"]["name"])
            window.setProperty("currArtist", trackData["json"]["artists"][0]["name"])

def getTrackData(lastTrackId, accessToken, accessTokenExpire):
    trackId = getTrackId()
    if(trackId == None or trackId == lastTrackId):
        return None

    currTime = int(time.time())

    if currTime >= accessTokenExpire:
        addon = xbmcaddon.Addon('plugin.audio.spotifyd-client')
        clientId = addon.getSetting('clientId')
        clientSecret = addon.getSetting('clientSecret')

        b64 = base64.b64encode(f'{clientId}:{clientSecret}'.encode('ascii')).decode('ascii')
        headers = {'Authorization': f'Basic {b64}'}
        body = {'grant_type': 'client_credentials'}
        response = requests.post(SPOTIFY_API_URL_TOKEN, headers=headers, data=body)
        accessToken = response.json()['access_token']
        accessTokenExpire = currTime + response.json()['expires_in']

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
    }
    response = requests.get(SPOTIFY_API_URL_TRACK + trackId, headers=headers)
    return {
        'accessToken': accessToken,
        'accessTokenExpire': accessTokenExpire,
        'lastTrackId': trackId,
        'json': response.json()
    }

def getTrackId():
    addonPath = service.getAddonPath()
    f = open(f'{addonPath}songs.log', 'r', -1, 'utf-8')
    songLog = f.read().splitlines()
    f.close()
    songLog = [k for k in songLog if '"PLAYER_EVENT": "play"' in k]
    if len(songLog) == 0:
        return None
    songLine = songLog[len(songLog)-1]
    x = songLine.find('"TRACK_ID":')
    return songLine[x+13:x+13+22]

def updateAlbumArt(lastTrackId, currTrackId, images):
    addonPath = service.getAddonPath()
    lastTrackPath = f'{addonPath}albumArt/{lastTrackId}'
    currTrackPath = f'{addonPath}albumArt/{currTrackId}'

    if lastTrackId == currTrackId:
        return lastTrackPath

    os.system(f'rm {addonPath}albumArt/*')
    
    images = sorted(images, key=lambda d: d['width'], reverse=False)

    #HQ
    res = requests.get(images[len(images)-1]["url"], stream = True)
    if res.status_code == 200:
        with open(currTrackPath + '.jpg', 'wb') as f:
            shutil.copyfileobj(res.raw, f)

    #LQ
    res = requests.get(images[0]["url"], stream = True)
    if res.status_code == 200:
        with open(currTrackPath + '_b.jpg', 'wb') as f:
            shutil.copyfileobj(res.raw, f)

    img = Image.open(currTrackPath + '_b.jpg')
    blur = img.filter(ImageFilter.GaussianBlur(9))
    blur.save(currTrackPath + '_b.jpg')
    blur_l = blur.convert('L')
    lightnessMap = []
    lightness = 0
    for loc in LIGHTNESS_PIXEL_LOCATIONS:
        currLoc = tuple(x * y for x, y in zip(blur.size, loc))
        lightnessMap.append(blur_l.getpixel(currLoc))
    for l in lightnessMap:
        lightness += l
    lightness = lightness / len(lightnessMap)
    return {
        'path': currTrackPath,
        'txtCol': 'FFFFFFFF' if lightness < 200 else 'FF000000'
    }



if (__name__ == '__main__'):
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    xbmc.executebuiltin('InhibitScreensaver(true)')
    ui = GUI('w_main.xml', service.getAddonPath(), 'default', '1080i', True, optional1='data')
    update_thread = threading.Thread(target=updateTrackData, args=(ui,))
    update_thread.daemon = True
    update_thread.start()
    ui.doModal()
    del ui
