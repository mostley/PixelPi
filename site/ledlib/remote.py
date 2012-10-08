import socket, math
from vector import *

PIXEL_SIZE = 3
PIXEL_DIM_X = 12
PIXEL_DIM_Y = 8
BUFFER_SIZE = PIXEL_DIM_X * PIXEL_DIM_Y * PIXEL_SIZE

class Remote:

    def __init__(self):
        self.UDP_IP = '127.0.0.1'
        self.UDP_PORT = 6803
        self.verbose = False

    def sendGrid(self, grid):
        bytedata = self.toByteArray(grid)
        self.sendBytes(bytedata)

    def sendBytes(self, bytedata):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto( bytedata, (self.UDP_IP, self.UDP_PORT) )

    def toByteArray(self, grid):
        result = bytearray(BUFFER_SIZE)

        i = 0
        while i < BUFFER_SIZE:
            y = i/3 % PIXEL_DIM_Y
            x = int(math.floor(i/3 / PIXEL_DIM_Y))
            if x % 2 == 0:
                c = grid[x][y]
                result[i] = c[0]
                i = i + 1
                result[i] = c[1]
                i = i + 1
                result[i] = c[2]
                i = i + 1
            else:
                c = grid[x][(PIXEL_DIM_Y-1)-y]
                result[i] = c[0]
                i = i + 1
                result[i] = c[1]
                i = i + 1
                result[i] = c[2]
                i = i + 1

        return result

    def createGridBuffer(self, color):
        result = []
        for x in range(PIXEL_DIM_X):
            result.append([])
            for y in range(PIXEL_DIM_Y):
                result[x].append(color)
        return result
    
    def setPixel(self, grid, v, color):
        pos = v.toIntArr()
        if pos[0] >= 0 and pos[0] < PIXEL_DIM_X and \
           pos[1] >= 0 and pos[1] < PIXEL_DIM_Y:
            grid[pos[0]][pos[1]] = color

    def clearPixels(self, grid, color):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = color


