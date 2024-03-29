import time
import argparse
import sys
import numpy as np

from Display_Enums import Operation, Dimensions
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


# Write graphics to the panels
class Panel_Writer():
    def __init__(self, borderColour,  *args, **kwargs):
            #super(RunText, self).__init__(*args, **kwargs)

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-r", "--led-rows", action="store", help=f"Display rows. 16 for 16x32, 32 for 32x32. Default: {Dimensions.DISPLAY_HEIGHT}", default=Dimensions.DISPLAY_HEIGHT, type=int)
        self.parser.add_argument("--led-cols", action="store", help=f"Panel columns. Typically 32 or 64. Default: {Dimensions.DISPLAY_WIDTH}", default=Dimensions.DISPLAY_WIDTH, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help=f"Daisy-chained boards. Default: {Dimensions.DISPLAY_CHAIN_LEN}", default=Dimensions.DISPLAY_CHAIN_LEN, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct", default=0, type=int, choices=[0,1,2,3,4])
        self.parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven... (Default: 0)", default=0, type=int)
        self.parser.add_argument("--led-panel-type", action="store", help="Needed to initialize special panels. Supported: 'FM6126A'", default="", type=str)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.args = self.parser.parse_args()

        self.stringArray = [[""], [""]]
        #self.artwork = 
        self.fontColour = []
        self.offset = 0
        self.graphicLength = []
        self.scrollIdxs = []
        self.mode = Operation.OFF
        self.updateDisplay = False
        self.musicClass = None
        self.newsClass = None



    def process(self):
        options = RGBMatrixOptions()
        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        options.panel_type = self.args.led_panel_type

        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio

        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options = options)

        self.run()

        return True


    def drawBorder(self, canvas, borderColour, rows, cols):
        graphics.DrawLine(canvas, 0, 0, 0, rows, borderColour)
        graphics.DrawLine(canvas, 0, rows, cols, rows, borderColour)
        graphics.DrawLine(canvas, cols, rows, cols, 0, borderColour)
        graphics.DrawLine(canvas, 0, 0, cols, 0, borderColour)
        return canvas

    def scrollStep(self, canvas, interval=None, intervalRatio=1, lrRatio=1.3):
        interval *= 1e9      
        for i, gLen in enumerate(self.graphicLength):
            if gLen < canvas.width:
                self.scrollIdxs[i] = 0
                continue


            if gLen < lrRatio * canvas.width:
                if (self.scrollIdxs[i] == canvas.width - gLen and
                 (self.scrollDirs[i][0]) != 1):
                    # Reached end of scroll
                    self.scrollDirs[i][0] = 1
                    self.scrollDirs[i][1] = 0
                    self.scrollDirs[i][2] = time.time_ns()

                elif (self.scrollIdxs[i] == 0 and
                 (self.scrollDirs[i][0]) != -1):
                    # At start of scroll
                    self.scrollDirs[i][0] = -1
                    self.scrollDirs[i][1] = 0
                    self.scrollDirs[i][2] = time.time_ns()

                if (time.time_ns() - self.scrollDirs[i][2]) > 1e9:
                    self.scrollDirs[i][1] = self.scrollDirs[i][0]


            if interval is not None:
                curTime = time.time_ns()
                if curTime - self.timeDeltas[i] > interval * (intervalRatio ** i):
                    self.scrollIdxs[i] += self.scrollDirs[i][1]
                    self.timeDeltas[i] = curTime
            
            else:
                self.scrollIdxs[i] += self.scrollDirs[i][1]

            if gLen >= lrRatio * canvas.width:
                if self.scrollIdxs[i] + gLen < 0:
                    self.scrollIdxs[i] = canvas.width


    def multiLine(self, canvas, numLines, font, colour, 
        height=Dimensions.DISPLAY_HEIGHT):
        self.graphicLength = []
        if numLines != 0:
            step = height // numLines
            for i in range(numLines):
                self.graphicLength.append(graphics.DrawText(
                    canvas, font, self.scrollIdxs[i], step * (i + 1) - 1,
                    colour, self.stringArray[i][0])) #
        return canvas


    #def drawArt(self, canvas, )

    def setGraphArray(self):
        ns_start = time.time_ns()
        self.scrollIdxs = [0 for i in self.stringArray]
        self.scrollDirs = [[1, -1, ns_start] for i in self.stringArray]
        self.timeDeltas = [ns_start for i in self.stringArray]


    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        fontMusic = graphics.Font()
        fontNews = graphics.Font()
        fontClock = graphics.Font()
        fontMusic.LoadFont("fonts/6x10.bdf")
        fontNews.LoadFont("fonts/7x14.bdf")
        fontClock.LoadFont("fonts/6x12.bdf")
        textColour = graphics.Color(0, 0, 255)
        textColour2 = graphics.Color(0, 255, 0)
        colourNews = graphics.Color(255, 0, 0)
        colourClock = graphics.Color(0, 255, 0)
        borderNews = graphics.Color(0,0,255)
        borderColour = graphics.Color(0, 255, 0)
        borderClock = graphics.Color(0, 0, 255)
        borderMusic = graphics.Color(255, 0, 0)
        pos1 = canvas.width
        pos2 = canvas.width
        self.scrollIdxs = []
        self.scrollDirs = []
        self.timeDeltas = []
        prevStringArray = []


        timestamp = ""
        self.matrix.brightness = 60
        rows = self.matrix.height
        cols = self.matrix.width
        while 1:
            curTime = time.time_ns()
            while self.mode == Operation.MUSIC:

                if self.musicClass.data is None:
                    continue

                if (time.time_ns() - curTime > 1e9) or self.scrollIdxs == []:
                    curTime = time.time_ns()
                    if (self.musicClass.data["title"].upper() != self.stringArray[0][0] and
                        self.musicClass.data["artist"].upper() != self.stringArray[1][0]):
                        self.stringArray = ([[self.musicClass.data["title"].upper()],
                            [self.musicClass.data["artist"].upper()]])
                        self.setGraphArray()

                canvas.Clear()
                canvas = self.multiLine(canvas, len(self.stringArray), 
                    fontMusic, textColour)
                self.scrollStep(canvas, 0.02, 1.3)
                #canvas = self.drawBorder(canvas, borderMusic, rows-1, cols-1)
                canvas = self.matrix.SwapOnVSync(canvas)

            while self.mode == Operation.NEWS:
                if self.newsClass.headlines is None:
                    continue

                if (time.time_ns() - curTime > 5e9) or self.scrollIdxs == []:
                    if ["      ".join(self.newsClass.headlines)] != self.stringArray[0]:
                        self.stringArray = [["      ".join(self.newsClass.headlines)],
                            ["      ".join(self.newsClass.headlines)]]
                        self.setGraphArray()

                canvas.Clear()
                canvas = self.multiLine(canvas, 1, fontNews, colourNews)
                self.scrollStep(canvas, 0.01, 1.3)
                self.drawBorder(canvas, borderNews, rows-1, cols-1)
                canvas = self.matrix.SwapOnVSync(canvas)

            while self.mode == Operation.CLOCK:
                while time.strftime('%H:%M') != timestamp:
                     timestamp = time.strftime('%H:%M')
                     canvas.Clear()
                     pos = 1
                     self.drawBorder(canvas, borderClock, rows-1, cols-1)
                     len1 = graphics.DrawText(canvas, fontClock, pos, 11,
                        colourClock, timestamp[0:5])
                     canvas = self.matrix.SwapOnVSync(canvas)

            while self.mode == Operation.OFF:
                if 'newCanvas' not in locals():
                    newCanvas = None
                curCanvas = canvas
                if newCanvas != curCanvas:
                    print("Clearing display")
                    timestamp = ""
                    newCanvas = curCanvas
                    canvas.Clear()
                    self.matrix.SwapOnVSync(canvas)    


                #canvas.Clear()
                #canvas = self.matrix.SwapOnVSync(canvas)
        canvas.Clear() 
        self.matrix.SwapOnVSync(canvas)    
        print("Broke out of operation while loop")