#!/usr/bin/env python

import colorsys
import time

try:
    import blinkt as blnkt
    blnkt.set_brightness(.1)
except ImportError:
    print "no Blinkt! found"



def pomodoro_fade(color = (255,0,0), min=25):
    blnkt.set_all(color[0], color[1], color[2])
    blnkt.show()
    for p in range(8):
        for i in range(1, 256):
            time.sleep(min*60/8/255.0)
            r, g, b = [x-i if x > 0 else 0 for x in color]
            blnkt.set_pixel(p, r, g, b)
            blnkt.show()
    blnkt.set_all(color[0], color[1], color[2], brightness = .1)
    blnkt.show()
    for i in range(4):
        blnkt.set_brightness(.2)
        blnkt.show()
        time.sleep(.1)
        blnkt.set_brightness(.1)
        blnkt.show()
        time.sleep(.1)

if __name__ == "__main__":
    while 1: 
        #Standard Pomodoro technique schedule:
        for i in range(4):
            pomodoro_fade(color = (255, 0, 0), min=25)
            pomodoro_fade(color=(0,255,0), min=5)
        pomodoro_fade(0,0,255, min=20)
