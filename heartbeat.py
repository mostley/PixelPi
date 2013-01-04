import time, random
from math import *
from game.librgb import *

class Heartbeat:

	def __init__(self):
		self.rgb = RGB(ip="127.0.0.1")

		self.running = True

		self.t = 0
		self.center = Vector(PIXEL_DIM_X/2, PIXEL_DIM_Y/2)
		self.maxDistance = self.center.getLength

	def update(self):
		self.t = ((math.sin(time.time())/2) + 0.5) * 0.8 + 0.2

		#self.center = Vector(PIXEL_DIM_X/2 - math.sin(time.time()*2), PIXEL_DIM_Y/2 + math.cos(time.time()*2))
	
	def getColor(self, v):
		distance = Vector.distance(self.center, v)
		distance = ((self.center.getLength()-distance) / self.center.getLength()) * 255
		distance *= self.t
		if distance > 255: 
			print "255"
			distance = 255
		if distance < 0: 
			print "0"
			distance = 0
		return (distance, 0, 0)

	def draw(self):

		for x in range(PIXEL_DIM_X):
			for y in range(PIXEL_DIM_Y):
				v = Vector(x,y)
				c = self.getColor(v)
				self.rgb.setPixel(v, c)

		self.rgb.send()

	def run(self):
		while self.running:
			self.update()
			self.draw()

if __name__ == "__main__":
	heartbeat = Heartbeat()
	heartbeat.run()