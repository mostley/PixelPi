#!/usr/bin/python
# -*- coding: utf8 -*- 

from evdev import *
from librgb import *
import time, random

COLORS = [BLACK, BLUE, RED, YELLOW, PURPLE, GREEN, ORANGE, TURQUE]

class Shape:
    def __init__(self, data):
        self.data = data
        self.rotation = 0
        self.position = Vector(PIXEL_DIM_X - 1, PIXEL_DIM_Y/2 - len(data[0]))
        self.lastDrop = time.time()
        self.colorIndex = 1

    def rotate(self):
        self.rotation += 1
        if self.rotation > len(self.data):
            self.rotation = 0
    
    def moveRight(self):
        if self.position.y < PIXEL_DIM_Y - 1:
            self.position.y += 1

    def moveLeft(self):
        if self.position.y > 0:
            self.position.y -= 1
    
    def rotateRandom(self):
        self.rotation = random.randrange(0, len(self.data))

    def canBePlaced(self, table):
        result = True

        for y in range(len(self.data[self.rotation])):
            for x in range(len(self.data[self.rotation][y])):
                if self.data[self.rotation][y][x]:
                    pos = self.position - Vector(x, y)
                    
                    if table[pos.y][pos.x] != 0:
                        result = False
                        break

        return result

    def canDrop(self, table):
        result = True

        for y in range(len(self.data[self.rotation])):
            for x in range(len(self.data[self.rotation][y])):
                if self.data[self.rotation][y][x]:
                    pos = self.position - Vector(x + 1, y)
                    
                    if pos.x < 0 or table[pos.y][pos.x] != 0:
                        result = False
                        break


        return result

    def update(self, interval):
        if (time.time() - self.lastDrop) > interval:
            self.position += Vector(-1, 0)

    def draw(self, rgb):
        for y in range(len(self.data[self.rotation])):
            for x in range(len(self.data[self.rotation][y])):
                if self.data[self.rotation][y][x]:
                    rgb.setPixel(self.position - Vector(x,y), COLORS[self.colorIndex])

    def writeTo(self, table):
        for y in range(len(self.data[self.rotation])):
            for x in range(len(self.data[self.rotation][y])):
                if self.data[self.rotation][y][x]:
                    pos = self.position - Vector(x,y)
                    table[pos.y][pos.x] = self.colorIndex

class Main:
    def __init__(self):
        self.rgb = RGB("127.0.0.1")# "192.168.1.5")
        self.rgb.invertedX = True
        self.rgb.invertedY = True
        self.keyboard = Device("/dev/input/event0")
        self.character = Vector(0,0)
        self.lastFrame = time.time()

        self.backgroundColor = BLACK

        self.table = self.createTable()

        self.currentShape = None
        self.lastShape = time.time()
        self.currentDropInterval = 2
        self.shapeInterval = 1.5
        self.temporaryFastDropInterval = 0.2
        self.isDroppingFast = False
        self.gameLost = False

        self.shapes = [

            # == L Shape ==
            Shape([[
                [True , True],
                [False, True],
                [False, True]
            ],[
                [False, False, True],
                [True , True , True]
            ],[
                [True , False],
                [True , False],
                [True , True ]
            ],[
                [True , True , True ],
                [True , False, False]
            ]]),

            # == inverse L Shape ==
            Shape([[
                [True , True],
                [True , False],
                [True , False]
            ],[
                [True , True , True],
                [False, False, True]
            ],[
                [False, True ],
                [False, True ],
                [True , True ]
            ],[
                [True , False, False],
                [True , True , True ]
            ]]),

            # == I Shape ==
            Shape([[
                [True],
                [True],
                [True],
            ],[
                [True , True , True]
            ]]),

            # == block Shape ==
            Shape([[
                [True, True],
                [True, True],
            ]]),

            # == Z Shape ==
            Shape([[
                [True , True, False],
                [False, True, True ],
            ],[
                [False, True ],
                [True , True ],
                [True , False],
            ]]),

            # == inverse Z Shape ==
            Shape([[
                [False, True, True ],
                [True , True, False],
            ],[
                [True , False],
                [True , True ],
                [False, True ],
            ]]),

            # == pyramid Shape ==
            Shape([[
                [False, True , False],
                [True , True , True ],
            ],[
                [True , False],
                [True , True ],
                [True , False],
            ],[
                [True , True , True ],
                [False, True , False],
            ],[
                [False, True ],
                [True , True ],
                [False, True ],
            ]])
        ]

    def createTable(self):
        return [[0 for i in range(PIXEL_DIM_X)] for i in range(PIXEL_DIM_Y)]

    def getKey(self, key):
        return key in self.keyboard.buttons and self.keyboard.buttons[key]

    def handleInput(self):
        if self.currentShape:
            if self.getKey("KEY_LEFT"):
                self.currentShape.moveLeft()
            if self.getKey("KEY_RIGHT"):
                self.currentShape.moveRight()
            if self.getKey("KEY_DOWN"):
                self.isDroppingFast = True
            if self.getKey("KEY_UP"):
                self.currentShape.rotate()
            if self.getKey("KEY_RETURN"):
                self.gameLost = False
                self.table = self.createTable()

    def removeFullRows(self):
        fullRows = []
        for y in range(len(self.table)):
            isFull = True
            for x in range(len(self.table[y])):
                if self.table[y][x] == 0:
                    isFull = False
            if isFull:
                fullRows.append(y)

        for y in fullRows:
            self.table.pop(y)
            self.table.append([0 for x in range(PIXEL_DIM_X)])

    def update(self):
        if self.gameLost:
            done = False
            for x in range(len(self.table[0])):
                for y in range(len(self.table)):
                    if self.table[y][x] == 0:
                        self.table[y][x] = random.randrange(1, len(COLORS))
                        done = True
                        break
                if done: break

        elif self.currentShape:
            if self.currentShape.canDrop(self.table):
                interval = self.currentDropInterval
                if self.isDroppingFast:
                    interval = self.temporaryFastDropInterval
                
                self.currentShape.update(interval)
            else:
                self.currentShape.writeTo(self.table)
                self.currentShape = None
                self.isDroppingFast = False
                self.lastShape = time.time()

                self.removeFullRows()
        elif (time.time() - self.lastShape) < self.shapeInterval:
            self.currentShape = random.choice(self.shapes)
            self.currentShape.colorIndex = random.randrange(1,len(COLORS))
            self.currentShape.position = Vector(PIXEL_DIM_X - 1, PIXEL_DIM_Y/2)
            self.currentShape.rotateRandom()

            if not self.currentShape.canBePlaced(self.table):
                self.gameOver()

    def gameOver(self):
        self.gameLost = True
        self.currentShape = None
        self.isDroppingFast = False
    
    def draw(self):
        for y in range(PIXEL_DIM_Y):
            for x in range(PIXEL_DIM_X):
                if self.table[y][x] != 0:
                    c = self.table[y][x]
                    self.rgb.setPixel(Vector(x,y), COLORS[c])

        if self.currentShape:
            self.currentShape.draw(self.rgb)

    def run(self):
        while True:
            self.lastFrame = time.time()
            self.rgb.clear(self.backgroundColor)

            self.handleInput()

            self.update()

            self.draw()

            self.rgb.send()
            
            while (time.time() - self.lastFrame) < 0.1:
                self.keyboard.poll()
                #time.sleep(0.4)

if __name__ == "__main__":
    main = Main()
    main.run()


