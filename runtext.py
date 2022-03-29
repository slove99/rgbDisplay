#!/usr/bin/env python
# Display a runtext with double-buffering.
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
import argparse
import sys
CLOCK = 1
MUSIC = 2
NEWS = 3
OFF = 0

# Scroll text across the panel
class RunText():
        def __init__(self, borderColor,  *args, **kwargs):
                #super(RunText, self).__init__(*args, **kwargs)

                self.parser = argparse.ArgumentParser()

                self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 16", default=16, type=int)
                self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=32, type=int)
                self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 2.", default=2, type=int)
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
                self.stringArray = [["test"], ["song"]]
                self.scrollStyle = []
                self.fontColor = []
                self.offset = 0
                self.mode = OFF
                self.updateDisplay = False



        def process(self):
                self.args = self.parser.parse_args()

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

                try:
                    # Start loop
                    print("Press CTRL-C to stop sample")
                    self.run()
                except KeyboardInterrupt:
                    print("Exiting\n")
                    sys.exit(0)

                return True


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
                fontMusic.LoadFont("fonts/6x10.bdf")
                fontNews.LoadFont("fonts/7x14.bdf")
                fontClock.LoadFont("fonts/6x12.bdf")
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
