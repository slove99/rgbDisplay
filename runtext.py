#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
CLOCK = 1
MUSIC = 2
NEWS = 3
OFF = 0
class RunText(SampleBase):
        def __init__(self, borderColor,  *args, **kwargs):
                super(RunText, self).__init__(*args, **kwargs)
                self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
                self.stringArray = [["test"], ["song"]]
                self.scrollStyle = []
                self.fontColor = []
                self.offset = 0
                self.mode = OFF
                self.updateDisplay = False

        def drawBorder(self, offscreen_canvas, borderColor, rows, cols):
                border = graphics.DrawLine(offscreen_canvas, 0, 0, 0, rows, borderColor)
                border = graphics.DrawLine(offscreen_canvas, 0, rows, cols, rows, borderColor)
                border = graphics.DrawLine(offscreen_canvas, cols, rows, cols, 0, borderColor)
                border = graphics.DrawLine(offscreen_canvas, 0, 0, cols, 0, borderColor)


        def run(self):
                offscreen_canvas = self.matrix.CreateFrameCanvas()
                fontMusic = graphics.Font()
                fontNews = graphics.Font()
                fontClock = graphics.Font()
                fontMusic.LoadFont("../../../../fonts/6x10.bdf")
                fontNews.LoadFont("../../../../fonts/7x14.bdf")
                fontClock.LoadFont("../../../../fonts/6x12.bdf")
                textColor = graphics.Color(0, 0, 255)
                textColor2 = graphics.Color(0, 255, 0)
                colorNews = graphics.Color(255, 0, 0)
                colorClock = graphics.Color(0, 255, 0)
                borderNews = graphics.Color(0,0,255)
                borderColor = graphics.Color(0, 255, 0)
                borderClock = graphics.Color(0, 0, 255)
                pos1 = offscreen_canvas.width
                pos2 = offscreen_canvas.width
                timestamp = ""
                self.matrix.brightness = 20
                rows = self.matrix.height
                cols = self.matrix.width
                print(rows)
                print(cols)
                while(1):
                        while(self.mode == MUSIC):
                                offscreen_canvas.Clear()
                                for i in range(len(self.stringArray)):
                                        len1 = graphics.DrawText(offscreen_canvas, fontMusic, pos1, 7, textColor, self.stringArray[0][0])
                                        len2 = graphics.DrawText(offscreen_canvas, fontMusic, pos2, 15, textColor2, self.stringArray[1][0])
                                pos1 -= 1
                                pos2 -= 1
                                if (pos1 + len1 < 0):
                                         pos1 = offscreen_canvas.width
                                if (pos2 + len2 < 0):
                                         pos2 = offscreen_canvas.width
                                time.sleep(0.04)
                                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        while(self.mode == NEWS):
                                offscreen_canvas.Clear()
                                len1 = graphics.DrawText(offscreen_canvas, fontNews, pos1, 12, colorNews, "         ".join(self.stringArray[0]))
                                self.drawBorder(offscreen_canvas, borderNews, rows-1, cols-1)
                                pos1 -= 1 # Careful
                                if (pos1 + len1 < 0):
                                         pos1 = offscreen_canvas.width
                                time.sleep(0.04)
                                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        while(self.mode == CLOCK):
                                while (time.strftime('%H:%M') != timestamp):
                                         timestamp = time.strftime('%H:%M')
                                         print(timestamp)
                                         offscreen_canvas.Clear()
                                         pos = 1
                                         self.drawBorder(offscreen_canvas, borderClock, rows-1, cols-1)
                                         len1 = graphics.DrawText(offscreen_canvas, fontClock, pos, 11, colorClock, timestamp[0:5])
                                         offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                        offscreen_canvas.Clear()
