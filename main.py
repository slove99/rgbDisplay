import time
from Music import Music
from News import News
import threading
mode = 0

SCROLL_STATIC = 0
SCROLL_FULL = 1
SCROLL_REVERSE = 2
SCROLL_STOP = 3
BORDER_COLOUR = 0


def newsThread():
    while 1:
        if(mode == 1):
            newsClass.updateAttributes()
            time.sleep(2)

def musicThread():
    while 1:
        if(mode == 2):
            musicClass.updateAttributes()
            time.sleep(1)

def displayThread():
    while 1:
        time.sleep(1)

# Function used to extract meaningful data to be displayed on the screen as well as information on how to display it
# INPUT: N/A
# OUTPUT: A  nested list of string arrays containing information to be displayed - an array for each row?
#         Number of rows to display at a time
#         Scrolling style for each row

def dataStructureThread():
    scrollStyle = []
    stringArray = []
    stringArray
    n = 3
    m = 4
    a = [[0] * m for i in range(n)]
    while 1:
        # Extract music data into the specified format and explain how to present it
        if(mode == 2):
            if(musicClass.nowPlaying != [] and musicClass.nowPlaying != None):
                stringArray.append([musicClass.nowPlaying.title])
                stringArray.append([musicClass.nowPlaying.get_artist().get_name()])
                scrollStyle.append(SCROLL_REVERSE)
                scrollStyle.append(SCROLL_REVERSE)

        if(mode == 1):
            scrollStyle.append(SCROLL_FULL)
            stringArray.append(newsClass.descriptions)


# Should specify how data should be displayed 2 col or 1 col, static, scroll full or scroll stop, or scroll back and forth
# Scroll mode:
    #Scroll fully until offscreen loop
    #Scroll and stop at end and reset
    # Scroll stop at end and go back
    # No scroll
#def driveDisplay(rows, scrollmode): # Should probably center by default if scrolling is set to static and center y wrt font size and row height


if __name__ == '__main__':
    musicClass = Music()
    newsClass = News()
    n = threading.Thread(target=newsThread)
    s = threading.Thread(target=displayThread)
    m = threading.Thread(target=musicThread)
    d = threading.Thread(target=dataStructureThread)

    n.start()
    s.start()
    m.start()
    d.start()
    while 1:
        mode = int(input("Enter mode"))
