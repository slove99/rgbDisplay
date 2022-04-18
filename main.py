import time
import threading
from datetime import datetime, time as t
import numpy as np

from Display_Enums import Operation
from Panel_Writer import Panel_Writer
from rgbmatrix import graphics
from Music import Volumio_Music
from News import News


global mode
global updateDisplay
mode = Operation.CLOCK
global stringArray
global fontColour
stringArray = []
updateDisplay = False


def newsThread():
    global mode
    while 1:
        if panelClass.mode == Operation.NEWS:
            print("Mode is News")
            newsClass.updateAttributes()
            time.sleep(15)

def musicThread():
    global mode
    while 1:
        if panelClass.mode == Operation.MUSIC:
            musicClass.updateAttributes()
            time.sleep(3)
        else:
            musicClass.updateAttributes()
            time.sleep(10)


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
    global fontColour
    panelClass.process()

if __name__ == '__main__':
    panelClass = Panel_Writer(graphics.Color(0, 255, 0))
    musicClass = Volumio_Music()
    panelClass.musicClass = musicClass
    newsClass = News()
    panelClass.newsClass = newsClass
    n = threading.Thread(target=newsThread)
    m = threading.Thread(target=musicThread)
    c = threading.Thread(target=displayControllerThread)
    s = threading.Thread(target=schedulerThread)

    n.start()
    m.start()
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
