#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, argparse, socket, math
from vector import *

PIXEL_SIZE = 3
PIXEL_DIM_X = 12
PIXEL_DIM_Y = 8
BUFFER_SIZE = PIXEL_DIM_X * PIXEL_DIM_Y * PIXEL_SIZE

WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
TURQUE = [0,255,255]
YELLOW = [255,255,0]
BLACK = [0,0,0]
ORANGE = [255, 127, 0]
PURPLE = [128, 0, 128]

class SPIDevice:
    def __init__(self, device='/dev/spidev0.0'):
        #import RPi.GPIO as GPIO
        self.spidev = file(device, "wb")
        self.running = True

    def init(self):
        pass

    def tick(self):
        pass
    
    def write(self, buffer):
        self.spidev.write(buffer)
        self.spidev.flush()

class RGB:

    def __init__(self, ip=None, port=6803, verbose=False):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.verbose = verbose
        self.invertedX = False
        self.invertedY = False
        self.remote = self.UDP_IP != None

        self.device = None

        self.buffer = self._createGridBuffer()

    # ==================================================================================================
    # ====================      Private                       ==========================================
    # ==================================================================================================

    def _toByteArray(self):
        result = bytearray(BUFFER_SIZE)

        i = 0
        while i < BUFFER_SIZE:
            y = i/3 % PIXEL_DIM_Y
            x = int(math.floor(i/3 / PIXEL_DIM_Y))
            if x % 2 == 0:
                c = self.buffer[x][y]
                result[i] = c[0]
                i = i + 1
                result[i] = c[1]
                i = i + 1
                result[i] = c[2]
                i = i + 1
            else:
                c = self.buffer[x][(PIXEL_DIM_Y-1)-y]
                result[i] = c[0]
                i = i + 1
                result[i] = c[1]
                i = i + 1
                result[i] = c[2]
                i = i + 1

        return result

    def _createGridBuffer(self, color=BLACK):
        result = []
        for x in range(PIXEL_DIM_X):
            result.append([])
            for y in range(PIXEL_DIM_Y):
                result[x].append(color)
        return result

    def _sendBytes(self, bytedata):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto( bytedata, (self.UDP_IP, self.UDP_PORT) )

    def _writeBytes(self, bytedata):
        if not self.device:
            self.device = SPIDevice()
        self.device.write(bytedata)

    # ==================================================================================================
    # ====================      Public                         ==========================================
    # ==================================================================================================
    
    def setPixel(self, v, color):
        pos = v.toIntArr()
        if self.invertedX:
            pos[0] = (PIXEL_DIM_X - 1) - pos[0]
        if self.invertedY:
            pos[1] = (PIXEL_DIM_Y - 1) - pos[1]
        if pos[0] >= 0 and pos[0] < PIXEL_DIM_X and \
           pos[1] >= 0 and pos[1] < PIXEL_DIM_Y:
            self.buffer[pos[0]][pos[1]] = color

    def clear(self, color):
        for x in range(len(self.buffer)):
            for y in range(len(self.buffer[x])):
                self.buffer[x][y] = color

    def send(self):
        bytes = self._toByteArray()

        if self.remote:
            if self.verbose:
                print "sending to ",self.UDP_IP,":",self.UDP_PORT
                print "sending ",self.buffer
            
            self._sendBytes(bytes)
        else:
            if self.verbose:
                print "sending ",self.buffer
            self._writeBytes(bytes)


