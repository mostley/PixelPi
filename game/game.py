#!/usr/bin/python

from evdev import *
from librgb import *
import time

class Main:
    def __init__(self):
        self.rgb = RGB("192.168.1.5")
        self.rgb.invertedX = True
        self.rgb.invertedY = True
        self.keyboard = Device("/dev/input/event0")
        self.character = Vector(0,0)
        self.lastFrame = time.time()

    def getKey(self, key):
        return key in self.keyboard.buttons and self.keyboard.buttons[key]

    def run(self):
        while True:
            self.lastFrame = time.time()
            self.rgb.clear(BLACK)

            if self.getKey("KEY_LEFT"):
                self.character += Vector(-1,0)
            if self.getKey("KEY_RIGHT"):
                self.character += Vector(1,0)
            if self.getKey("KEY_UP"):
                self.character += Vector(0,1)
            if self.getKey("KEY_DOWN"):
                self.character += Vector(0,-1)
            self.character.x = self.character.x % PIXEL_DIM_X
            self.character.y = self.character.y % PIXEL_DIM_Y
            self.rgb.setPixel(self.character, RED)
            self.rgb.send()
            
            while (time.time() - self.lastFrame) < 0.1:
                self.keyboard.poll()

if __name__ == "__main__":
    main = Main()
    main.run()


