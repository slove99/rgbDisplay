import pylast
import requests
import numpy as np


class LastFM_Music:
    nowPlaying = [] # Store the currently playing song
    def __init__(self):
        credFile = open('cred.txt', 'r')
        self.username = next(credFile)[:-1]
        credPwd = next(credFile)[:-1]
        credAPIKey = next(credFile)[:-1]
        credAPISec = next(credFile)
        credPwdHash = pylast.md5(credPwd)
        while 1:
               try:
                   self.network = pylast.LastFMNetwork(api_key=credAPIKey, api_secret=credAPISec,
                                       username=self.username, password_hash=credPwdHash)
                   break
               except pylast.WSError:
                   print("Error creating self.network")
                   pass
        self.user = pylast.User(self.username, self.network)

    def getCurrentSong(self):
        return (self.user.get_now_playing())

    def updateAttributes(self):
        self.nowPlaying = self.getCurrentSong()


class Volumio_Music:
    api_url = "http://192.168.1.169/api/v1/getState"
    def __init__(self):
        self.data = None


    def getVolumioState(self):
        return self.data


    def updateAttributes(self):
        try:
            self.data = requests.get(self.api_url).json()
        except requests.exceptions.RequestException as e:
            print("Voluimio connection error")


    def getVolumioArt(self, x, y):
        url = request.get(self.data["albumart"])
        with Image.open(BytesIO(response.content)) as im:
            self.art = im.resize((x, y))
        