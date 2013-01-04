#!/usr/bin/python
# -*- coding: utf8 -*-

import time
from evdev import *

class ControllCenter:
	
	def __init__(self):
		self.lastFrame = 0
		self.keyboard = Device("/dev/input/event0")

	def execute(self, cmd):
		if cmd == "off":
			spidev = file("/dev/spidev0.0")
			spidev.write(bytearray([0 for i in range(125)]))
			spidev.flush()

	def handleInput(self):
		if self.getKey("KEY_F12"):
			self.execute("off")
	
	def getKey(self, key):
		 return key in self.keyboard.buttons and self.keyboard.buttons[key]

	def run(self):
		while True:
			self.lastFrame = time.time()
			
			self.handleInput()
			
			while (time.time() - self.lastFrame) < 0.1:
		        self.keyboard.poll()
		        time.sleep(0.2)
			                
if __name__ == "__main__":