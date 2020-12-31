import pylast
class Music:
    nowPlaying = [] # Store the currently playing song
    def __init__(self):
        credFile = open('cred.txt', 'r')
        self.username = next(credFile)[:-1]
        credPwd = next(credFile)[:-1]
        credAPIKey = next(credFile)[:-1]
        credAPISec = next(credFile)
        credPwdHash = pylast.md5(credPwd)
        self.network = pylast.LastFMNetwork(api_key=credAPIKey, api_secret=credAPISec,
                                       username=self.username, password_hash=credPwdHash)
        self.user = pylast.User(self.username, self.network)

    def getCurrentSong(self):
        return (self.user.get_now_playing())

    def updateAttributes(self):
        self.nowPlaying = self.getCurrentSong()