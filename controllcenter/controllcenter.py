#!/usr/bin/python
# -*- coding: utf8 -*-

import time
from evdev import *

class ControllCenter:
	
	def __init__(self):
		self.lastFrame = 0

	def handleInput(self):
		pass
	
	def getKey(self, key):
		pass
	
	def run(self):
		while True:
			self.lastFrame = time.time()
			
			self.handleInput()
			
			while (time.time() - self.lastFrame) < 0.1:
		        self.keyboard.poll()
		        time.sleep(0.2)
			                
if __name__ == "__main__":