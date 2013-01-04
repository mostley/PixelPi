#!/usr/bin/python
# -*- coding: utf8 -*-

### BEGIN INIT INFO
# Provides:          controllcenter
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start controllcenter daemon at boot time
# Description:       Enable service provided by daemon
### END INIT INFO

import time
from evdev import *

class ControllCenter:
	
	def __init__(self):
		self.lastFrame = 0
		self.keyboard = Device("/dev/input/event0")

	def execute(self, cmd):
		print "Executing ", cmd
		
		if cmd == "off":
			spidev = file("/dev/spidev0.0", "w")
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
	print "Starting Controll Center"
	center = ControllCenter()
	center.run()
	print "Controll Center is shutting down"