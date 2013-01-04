#!/usr/bin/python
#
# Copyright (c) 2012 SHDev - Sven Hecht
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
"""Img2GCode.py

Sends the image to the table

Usage: python sendimg.py [options] file

Options:
  -h, --help		show this help
  --ip 				the IP of the rgb
  --port			the Port of the rgb
  --scale			determines if the image should be scaled to fit

"""
from math import *
import sys, argparse, socket, math, getopt
from PIL import Image
from PIL import ImageOps
from PIL import ImageEnhance
from rgb import *
from vector import *


class Connector:
	"Class to handle generating gcode."

	def __init__(self, img_path, ip, port, scale, verbose):

		self.rgb = RGB(ip, port, verbose)
		self.file = img_path
		self.scale = scale

		self.load_image()

	def load_image(self):

		self.image = Image.open(self.file)

		self.width = self.image.size[0]
		self.height = self.image.size[1]
		self.data = self.image.getdata()

		if self.scale:
			self.data = self.scaleData()

	def addColor(self, c1, c2):
		return (c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])

	def getAverageColor(self, tx, ty):
		result = (0,0,0)
		index = 0

		xstep = self.width / PIXEL_DIM_X
		ystep = self.height / PIXEL_DIM_Y
		startx = xstep * tx
		starty = ystep * ty
		endx = startx + xstep - 1
		endy = starty + ystep - 1

		count = 0
		print len(self.data)

		print starty,endy

		for x in range(startx, startx + xstep):
			for y in range(starty, starty + ystep):
				index = y * self.width + x
				#print x,":",y,"->", y * self.width
				result = self.addColor(result, self.data[index])
				count += 1
		"""
				for j in range(len(self.data)):
					color = self.data[j]
					x = index % self.width
					y = int(index / self.width)
					index += 1

					if x >= startx and y >= starty and x <= endx and y <= endy:
						result = self.addColor(result, color)
						count += 1
		"""

		if count != 0:
			result = (result[0] / count, result[1] / count, result[2] / count)

		#print tx,":",ty,"->",result

		return result


	def scaleData(self):
		result = []

		for y in range(PIXEL_DIM_Y):
			for x in range(PIXEL_DIM_X):
				color = self.getAverageColor(x,y)
				result.append(color)

		return result

	def transmit(self):
		index = 0
		for color in self.data:
			x = index % self.width
			y = int(index / self.width)
			print x,y,color
			self.rgb.setPixel(Vector(x,y), color)

			index += 1

		self.rgb.send()

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "h", [
			"help",
			"ip=",
			"port=",
			"scale",
			"verbose"
		])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
        
	ip = '127.0.0.1'
	port = 6803
	scale = False
	verbose = False

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("--ip"):
			ip = arg
		elif opt in ("--port"):
			port = int(arg)
		elif opt in ("--scale"):
			scale = True
		elif opt in ("--verbose"):
			verbose = True

	connector = Connector(argv[-1], ip, port, scale, verbose)
	connector.transmit()

def usage():
    print __doc__

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1:])
	else:
		usage()