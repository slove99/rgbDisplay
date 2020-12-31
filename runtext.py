#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
        def __init__(self, borderColor,  *args, **kwargs):
                super(RunText, self).__init__(*args, **kwargs)
                self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
                self.stringArray = []
                self.scrollStyle = []
                self.fontColor = []
                self.offset = 0
                self.updateDisplay = False

        def run(self):
            #if (self.updateDisplay == True):
            #    if (len(self.stringArray) == 2):
            #       font.LoadFont("../../../fonts/4x6.bdf")
            #        offset = [2, 12]
            #    if (len(self.stringArray) == 1):
            #        font.LoadFont("../../../fonts/9x15.bdf")
            #        offset = [6]
                offscreen_canvas = self.matrix.CreateFrameCanvas()
                font = graphics.Font()
                font.LoadFont("../../../../fonts/6x12.bdf")
                textColor = graphics.Color(0, 0, 255)
                borderColor = graphics.Color(0, 255, 0)
                pos = offscreen_canvas.width
                timestamp = ""
                while(1):
                        while (time.strftime('%H:%M') != timestamp):
                                timestamp = time.strftime('%H:%M')
                                #print(timestamp)
                                #print(pos)
                                offscreen_canvas.Clear()
                                pos = 1
                                len = graphics.DrawText(offscreen_canvas, font, pos, 11, textColor, timestamp[0:5])
                                border = graphics.DrawLine(offscreen_canvas, 0, 0, 0, 15, borderColor)
                                border = graphics.DrawLine(offscreen_canvas, 0, 15, 31, 15, borderColor)
                                border = graphics.DrawLine(offscreen_canvas, 31, 15, 31, 0, borderColor)
                                border = graphics.DrawLine(offscreen_canvas, 0, 0, 31, 0, borderColor)
                #pos -= 1
                #if (pos + len < 0):
                #    pos = offscreen_canvas.width

                #time.sleep(0.05)
                                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
#if __name__ == "__main__":
#        borderColor = graphics.Color(255,255,255)
##        run_text = RunText(borderColor)
#        #run_text.run()
#        if (not run_text.process()):
#                run_text.print_help()
#        while(1):
#                print("test")
