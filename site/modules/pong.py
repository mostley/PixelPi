import time
from threading import Thread
from ledlib.colors import *
from ledlib.remote import *
from ledlib.vector import *

class Pong:
    def __init__(self):
        self.commands = ['pong_left_up', 'pong_left_down', 'pong_right_up', 'pong_right_down']
        self.remote = None
        self.grid = None
        self.leftPaddle = Vector(0,4)
        self.rightPaddle = Vector(11,4)
        self.ball = Vector(6,4)
        self.ballSpeed = 5
        self.ballvelocity = Vector(1,1)*self.ballSpeed
        self.thread = None
        self.running = False

    def init(self):
        self.remote = Remote()
        self.grid = self.remote.createGridBuffer(BLACK)
        self.remote.sendGrid(self.grid)

        try:
            self.thread = Thread(target=self.update, args=())
            self.thread.start()
        except Exception, errtxt:
            print errtxt

    def deinit(self):
        self.running = False

    def update(self):
        lastupdate = time.clock()
        self.running = True
        while self.running:
            t = time.clock()
            dt = (t - lastupdate)
            lastupdate = t
            
            #print "update",dt,self.ball,self.ballvelocity * dt
            self.ball += self.ballvelocity * dt
            
            self.draw()
            
            time.sleep(1/24.0)
    
    def draw(self):
        self.remote.clearPixels(self.grid, BLACK)
        
        self.remote.setPixel(self.grid, self.leftPaddle, BLUE)
        self.remote.setPixel(self.grid, self.rightPaddle, BLUE)
        self.remote.setPixel(self.grid, self.ball, WHITE)
        
        self.remote.sendGrid(self.grid)


    def execute(self, data):
        result = False
        
        if not self.remote:
            self.init()
        
        print "pong - executing command:" + data['command']
        if data['command'] == 'pong_left_up':
            self.leftPaddle.y += 1
            if self.leftPaddle.y > PIXEL_DIM_X - 1: self.leftPaddle.y = PIXEL_DIM_X - 1
        elif data['command'] == 'pong_left_down':
            self.leftPaddle.y -= 1
            if self.leftPaddle.y < 0: self.leftPaddle.y = 0
        elif data['command'] == 'pong_right_up':
            self.rightPaddle.y += 1
            if self.rightPaddle.y > PIXEL_DIM_X - 1: self.rightPaddle.y = PIXEL_DIM_X - 1
        elif data['command'] == 'pong_right_down':
            self.rightPaddle.y -= 1
            if self.rightPaddle.y < 0: self.rightPaddle.y = 0
        
        self.draw()
        
        result = True
        
        return result


def getModule():
    return Pong()

