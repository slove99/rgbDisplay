
import time
from datetime import datetime, time as t
from Music import Music
from News import News
import threading

from runtext import RunText

from samplebase import SampleBase
from rgbmatrix import graphics

SCROLL_STATIC = 0
SCROLL_FULL = 1
SCROLL_REVERSE = 2
SCROLL_STOP = 3
BORDER_COLOUR = 0

DISPLAY_HEIGHT = 16
DISPLAY_WIDTH = 32

global mode
global updateDisplay
mode = 2
global stringArray
global scrollStyle
global fontColour
stringArray = []
updateDisplay = False


def newsThread():
    global mode
    while 1:
        if(scrollerClass.mode == 3):
            print("Mode is 3")
            newsClass.updateAttributes()
            time.sleep(50)

def musicThread():
    global mode
    while 1:
        if(scrollerClass.mode == 2):
            musicClass.updateAttributes()
            time.sleep(10)
        else:
            musicClass.updateAttributes()
            time.sleep(20)
# Function used to extract meaningful data to be displayed on the screen as well as information on how to display it
# INPUT: N/A
# OUTPUT: A  nested list of string arrays containing information to be displayed - an array for each row?
#         Number of rows to display at a time
#         Scrolling style for each row

def dataStructure():
    global stringArray
    global mode
    scrollStyle = []
    fontColour = []
    stringArray = []
    scrollStyle = []
    # Extract music data into the specified format and explain how to present it
    if(scrollerClass.mode == 2):
        if(musicClass.nowPlaying != [] and musicClass.nowPlaying != None):
            stringArray.append([musicClass.nowPlaying.title])
            stringArray.append([musicClass.nowPlaying.get_artist().get_name()])
            scrollStyle.append(SCROLL_REVERSE)
            scrollStyle.append(SCROLL_REVERSE)
            fontColour.append(graphics.Color(255, 255, 0))
            fontColour.append(graphics.Color(0, 255, 0))

    if(scrollerClass.mode == 3):
        scrollStyle.append(SCROLL_FULL)
        stringArray.append(newsClass.descriptions[0:2])
        fontColour.append(graphics.Color(255, 255, 255))
    return stringArray, scrollStyle, fontColour

# Responsible for updating the string data to be sent to the display
def displayUpdaterThread(): # Should probably center by default if scrolling is set to static and center y wrt font size and row height
    global updateDisplay
    global stringArray
    global scrollStyle
    global fontColour
    while(1):
        stringArrayNew, scrollStyle, fontColour = dataStructure()
        if(stringArray != []):
            scrollerClass.stringArray = stringArray
        if stringArrayNew != stringArray:
            updateDisplay = True
            stringArray = stringArrayNew
            scrollerClass.stringArray = stringArray
        time.sleep(1)


def betweenTime(startTime, endTime, curTime=None):
    # If check time is not given, default to current UTC time
    curTime = curTime or datetime.utcnow().time()
    if startTime < endTime:
        return curTime >= startTime and curTime <= endTime
    else:
        return curTime >= startTime or curTime <= endTime


# Responsible for controlling what state the display should operate in
def schedulerThread():
    print("In schedulerThread")
    modeOFF = 0
    modeMIX = 1
    modeCLOCK = 2
    modeMUSIC = 3
    modeNEWS = 4
    mode = modeMIX
    timeON = t(7, 15)
    timeOFF = t(23, 55)
    while(1):
        curTime = datetime.now()
        curHours = int(curTime.strftime("%H"))
        curMins = int(curTime.strftime("%M"))
        if(betweenTime(timeON, timeOFF)):
            if(mode == modeOFF):
                scrollerClass.mode = 0
            if(mode == modeCLOCK):
                scrollerClass.mode = 3
            if(mode == modeMUSIC):
                scrollerClass.mode = 2
            if(mode == modeNEWS):
                scrollerClass.mode = 1
            if(mode == modeMIX):
                print("In mode MIX")
                if( (curMins >= 0 and curMins <= 15) or (curMins >= 30 and curMins <= 50) ):
                    print("Showing news")
                    scrollerClass.mode = 3
                elif (musicClass.nowPlaying != [] and musicClass.nowPlaying != None):
                    print("Showing music")
                    scrollerClass.mode = 2
                else:
                    print("Showing time")
                    scrollerClass.mode = 1
        else:
            print("Display off")
            scrollerClass.mode == 0
        time.sleep(15)


def displayControllerThread():
    global stringArray
    global scrollStyle
    global fontColour
    scrollerClass.process()

if __name__ == '__main__':
    musicClass = Music()
    newsClass = News()
    scrollerClass = RunText(graphics.Color(0, 255, 0))
    n = threading.Thread(target=newsThread)
    m = threading.Thread(target=musicThread)
    d = threading.Thread(target=displayUpdaterThread)
    c = threading.Thread(target=displayControllerThread)
    s = threading.Thread(target=schedulerThread)

    n.start()
    m.start()
    d.start()
    c.start()
    s.start()
    while 1:
        continue
