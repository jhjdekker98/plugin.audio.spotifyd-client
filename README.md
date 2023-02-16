# plugin.audio.spotifyd-client
A simple KODI client wrapper for [SpotifyD](https://github.com/Spotifyd/spotifyd)

---

### Foreword

The most recent go-to Spotify plugin for Kodi (https://github.com/ldsz/plugin.audio.spotify) seems to have been abandoned. I do not intend to create "the new Spotify plugin" for Kodi, but I do want an option for somewhat tech-savvy Kodi users to listen to Spotify through their Kodi installation.

**A SPOTIFY PREMIUM ACCOUNT IS NECESSARY FOR THE KODI PLUGIN TO WORK**

As of now (january 2023) - the plugin uses some specific folder locations only available on Linux-based installations of Kodi. Windows and Mac support are planned, but as of right now have no ETA yet. Windows support has some preferential treatment over Mac support, since I have no Apple machines or a hackintosh to test on.

---

### Installation

The installation process for the plugin is relatively simple, but requires a bit more work than your typical plugin installation in Kodi.

1. Download the source code ZIP for the GitHub repo using the `<> Code`-button on the main page of this repo.
1. Save the ZIP file to a location accessible to your Kodi installation - for example a USB flash drive or a network storage location.
1. Before installing the addon in Kodi, you need to compile SpotifyD for your target system. Refer to the `SpotifyD Compilation` section.
1. After compiling SpotifyD, place the binary in the `/resources/lib/spotifyd` directory with the name `spotifyd`. The full path to the compiled binary within the installation ZIP should be `/resources/lib/spotifyd/spotifyd`. If any of the directories do not yet exist, create them.
1. In Kodi, navigate to your addons and select the `Install from ZIP` option. Locate the updated ZIP-file containing the compiled binary and install it as usual.
1. Lastly, in Kodi, navigate to the addon settings. There are two input fields in the configuration that need to be set. The first one is the Client ID and the second one the Client Secret of your Spotify Developer app. If you do not have this information yet, refer to the `Spotify Developer` section.

### SpotifyD Compilation

Follow [the SpotifyD source compilation steps](https://spotifyd.github.io/spotifyd/installation/index.html) on your target machine. If you know how to cross-compile for different hardware, feel free to follow [the cross-compilation steps](https://github.com/Spotifyd/spotifyd/wiki/Cross-Compiling-on-Ubuntu) instead.

### Spotify Developer

In order to get the functionalities of the app to work, you need a Spotify Developer account and an app registered in the Spotify Developer dashboard.

1. Navigate to https://developer.spotify.com/dashboard/ and login with your Spotify Premium account.
1. Click the `CREATE AN APP`-button and enter an app name and description as wanted.
1. On the next page, take note of the Client ID and Client Secret (unhide by clicking `SHOW CLIENT SECRET`).

This information is necessary to get the SpotifyD Wrapper to work.
