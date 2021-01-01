import time
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
        if(mode == 3):
            print("Mode is 3")
            newsClass.updateAttributes()
            time.sleep(10)

def musicThread():
    global mode
    while 1:
        if(mode == 2):
            musicClass.updateAttributes()
            time.sleep(10)

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
    if(mode == 2):
        if(musicClass.nowPlaying != [] and musicClass.nowPlaying != None):
            stringArray.append([musicClass.nowPlaying.title])
            stringArray.append([musicClass.nowPlaying.get_artist().get_name()])
            scrollStyle.append(SCROLL_REVERSE)
            scrollStyle.append(SCROLL_REVERSE)
            fontColour.append(graphics.Color(255, 255, 0))
            fontColour.append(graphics.Color(0, 255, 0))

    if(mode == 3):
        scrollStyle.append(SCROLL_FULL)
        stringArray.append(newsClass.descriptions[0:2])
        fontColour.append(graphics.Color(255, 255, 255))
    return stringArray, scrollStyle, fontColour

# Should specify how data should be displayed 2 col or 1 col, static, scroll full or scroll stop, or scroll back and forth
# Scroll mode:
    #Scroll fully until offscreen loop
    #Scroll and stop at end and reset
    # Scroll stop at end and go back
    # No scroll
def displayUpdaterThread(): # Should probably center by default if scrolling is set to static and center y wrt font size and row height
    global updateDisplay
    global stringArray
    global scrollStyle
    global fontColour
    while(1):
        #print("Running")
        stringArrayNew, scrollStyle, fontColour = dataStructure()
        if(stringArray != []):
            scrollerClass.stringArray = stringArray
        if stringArrayNew != stringArray:
            updateDisplay = True
            stringArray = stringArrayNew
            scrollerClass.stringArray = stringArray
        time.sleep(1)

def displayControllerThread():
    global stringArray
    global scrollStyle
    global fontColour
    #offset = 0
    #offscreen_canvas = self.matrix.CreateFrameCanvas()
    #pos = offscreen_canvas.width
    #font = graphics.Font()
    scrollerClass.process()
    #while 1:
    #    if(updateDisplay == True):
    #        if(len(stringArray) == 2):
    #            font.LoadFont("../../../fonts/4x6.bdf")
    #            offset = [2, 12]
    #        if(len(stringArray) == 1):
    #            font.LoadFont("../../../fonts/9x15.bdf")
    #            offset = [6]

    #    for i in range(len(stringArray)):  # For each row
    #        # Perform scroll specific transformations
    #        len = graphics.DrawText(offscreen_canvas, font, pos, offset[i], fontColour[i], stringArray[i])
    #    pos -= 1
    #    if (pos + len < 0):
    #        pos = offscreen_canvas.width
    #    time.sleep(0.05)
    #    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)





    #textColor = graphics.Color(255, 255, 0)
    #pos = offscreen_canvas.width
    #my_text = self.args.text

    #while True:
    #    offscreen_canvas.Clear()
    #    len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
    #    pos -= 1
    #    if (pos + len < 0):
    #        pos = offscreen_canvas.width

    #    time.sleep(0.05)
    #    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == '__main__':
    musicClass = Music()
    newsClass = News()
    scrollerClass = RunText(graphics.Color(0, 255, 0))
    n = threading.Thread(target=newsThread)
    m = threading.Thread(target=musicThread)
    d = threading.Thread(target=displayUpdaterThread)
    c = threading.Thread(target=displayControllerThread)

    n.start()
    m.start()
    d.start()
    c.start()
    while 1:
        mode = 2 #int(input("Enter mode"))
