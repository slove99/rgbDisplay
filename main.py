import time
import threading
from datetime import datetime, time as t

from Display_Enums import Operation
from Panel_Writer import Panel_Writer
from rgbmatrix import graphics
from Music import Volumio_Music
from News import News



SCROLL_STATIC = 0
SCROLL_FULL = 1
SCROLL_REVERSE = 2
SCROLL_STOP = 3
BORDER_COLOUR = 0

global mode
global updateDisplay
mode = Operation.CLOCK
global stringArray
global scrollStyle
global fontColour
stringArray = []
updateDisplay = False


def newsThread():
    global mode
    while 1:
        if panelClass.mode == 3:
            print("Mode is 3")
            newsClass.updateAttributes()
            time.sleep(50)

def musicThread():
    global mode
    while 1:
        if panelClass.mode == 2:
            musicClass.getVolumioState()
            time.sleep(10)
        else:
            musicClass.updateAttributes()
            time.sleep(20)

# Function used to extract meaningful data to be displayed on the screen as well
# as information on how to display it
# INPUT: N/A
# OUTPUT: A  nested list of string arrays containing information to be displayed
# - an array for each row?
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
    if panelClass.mode == Operation.MUSIC:
        if musicClass.data != []:
            if musicClass.data["status"] == "play":
                stringArray.append([musicClass.data["title"].upper()])
                stringArray.append([musicClass.data["artist"].upper()])
                scrollStyle.append(SCROLL_REVERSE)
                scrollStyle.append(SCROLL_REVERSE)
                fontColour.append(graphics.Color(255, 255, 0))
                fontColour.append(graphics.Color(0, 255, 0))
            else:
                stringArray = ""


    if panelClass.mode == Operation.NEWS:
        scrollStyle.append(SCROLL_FULL)
        stringArray.append(newsClass.descriptions[0:2])
        fontColour.append(graphics.Color(255, 255, 255))
    return stringArray, scrollStyle, fontColour

# Responsible for updating the string data to be sent to the display
def displayUpdaterThread(): 
    # Should probably center by default if scrolling is 
    # set to static and center y wrt font size and row height
    global updateDisplay
    global stringArray
    global scrollStyle
    global fontColour
    while 1:
        stringArrayNew, scrollStyle, fontColour = dataStructure()
        if stringArray != []:
            panelClass.stringArray = stringArray
        if stringArrayNew != stringArray:
            updateDisplay = True
            stringArray = stringArrayNew
            panelClass.stringArray = stringArray
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
    global mode
    timeON = t(7, 15)
    timeOFF = t(22, 30)
    while 1:

        if 'curMode' not in locals():
            curMode = None

        if mode == curMode:
            time.sleep(1)
            continue

        curMode = mode
        curTime = datetime.now()
        curHours = int(curTime.strftime("%H"))
        curMins = int(curTime.strftime("%M"))
        if betweenTime(timeON, timeOFF):
            if mode == Operation.OFF:
                panelClass.mode = Operation.OFF
            if mode == Operation.CLOCK:
                panelClass.mode = Operation.CLOCK
            if mode == Operation.MUSIC:
                panelClass.mode = Operation.MUSIC
            if mode == Operation.NEWS:
                panelClass.mode = Operation.NEWS
            if mode == Operation.MIX:
                print("In mode MIX")
                if ((curMins >= 0 and curMins <= 15) or 
                    (curMins >= 30 and curMins <= 50)):
                    print("Showing news")
                    panelClass.mode = Operation.NEWS
                elif (musicClass.nowPlaying != [] and
                    musicClass.nowPlaying != None):
                    print("Showing music")
                    panelClass.mode = Operation.MUSIC
                else:
                    print("Showing time")
                    panelClass.mode = Operation.CLOCK
        else:
            print("Display off")
            panelClass.mode == Operation.OFF


def displayControllerThread():
    global stringArray
    global scrollStyle
    global fontColour
    panelClass.process()

if __name__ == '__main__':
    panelClass = Panel_Writer(graphics.Color(0, 255, 0))
    musicClass = Volumio_Music()
    newsClass = News()
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

    print("Type 'off' to turn off the panels")
    while 1:
        prevPanelState = panelClass.mode
        cmd = input("> ")
        if cmd.lower() == "off":
            prevPanelState = (panelClass.mode if panelClass.mode else 
            prevPanelState)
            mode = Operation.OFF
        if cmd.lower() == "on":
            mode = prevPanelState
        if cmd.lower() == "music":
            mode = Operation.MUSIC
        if cmd.lower() == "clock":
            mode = Operation.CLOCK
        if cmd.lower() == "news":
            mode = Operation.NEWS

        continue
