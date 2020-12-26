import time
from Music import Music
from News import News
import threading
mode = 0
def newsThread():
    while 1:
        if(mode == 1):
            time.sleep(2)
            newsHeadlines, newsDescriptions = newsClass.getNews()
            print(newsHeadlines[0])


def displayThread():
    while 1:
        time.sleep(1)


def musicThread():
    while 1:
        if(mode == 2):
            curSong = musicClass.getCurrentSong()
            if curSong != None:
                print(curSong.get_artist().name + curSong.get_name())
            time.sleep(1)

if __name__ == '__main__':
    musicClass = Music()
    newsClass = News()
    n = threading.Thread(target=newsThread)
    s = threading.Thread(target=displayThread)
    m = threading.Thread(target=musicThread)

    n.start()
    s.start()
    m.start()
    while 1:
        mode = int(input("Enter mode"))