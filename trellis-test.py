#Author: Becky Button
#This is a file to test the 4x4 trellis module, and
#test that the colors are being cycled correctly!

import time

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#create the trellis
trellis = NeoTrellis(i2c_bus)

#colors
OFF = (0,0,0)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 255)
GREEN  = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (46, 43, 95)
VIOLET = (139, 0, 255)

#this stores all of the possible color options
COLORS = [OFF, RED, ORANGE, YELLOW, GREEN, BLUE,\
     INDIGO, VIOLET]

#the current color index the given button is at
currentColor = [0] * 16

def changeColor(pixel):
    tempColor = currentColor[pixel] + 1
    tempColor %= len(COLORS)
    currentColor[pixel] = tempColor
    trellis.pixels[pixel] = COLORS[tempColor]

#this will be called when button events are received
def changeLEDState(event):
    #turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        #trellis.pixels[event.number] = CYAN
        changeColor(event.number)


for i in range(16):
    #activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)

    #set all keys to trigger the changeLEDState callback
    trellis.callbacks[i] = changeLEDState

for i in range(16):
    trellis.pixels[i] = currentColor[i]
    time.sleep(.05)

while True:
    #call the sync function call any triggered callbacks
    trellis.sync()
    #the trellis can only be read every 17 millisecons or so
    time.sleep(.02)
