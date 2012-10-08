import time, math
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
        self.ballSpeed = 10
        self.thread = None
        self.running = False
        self.reset()
        
        self.score = 0
        
        self.maxY = PIXEL_DIM_Y - 1
        self.maxX = PIXEL_DIM_X - 1

    def init(self):
        self.remote = Remote()
        self.grid = self.remote.createGridBuffer(BLACK)
        self.remote.sendGrid(self.grid)
        self.startTime = time.clock()

        try:
            self.thread = Thread(target=self.update, args=())
            self.thread.start()
        except Exception, errtxt:
            print errtxt

    def deinit(self):
        self.running = False
    
    def reset(self):
        self.ball = Vector(6,4)
        self.ballSpeed = 10
        self.ballvelocity = Vector.randomUnitCircle()*self.ballSpeed
        while abs(self.ballvelocity.x) < 0.1:
            self.ballvelocity = Vector.randomUnitCircle()*self.ballSpeed
        self.startTime = time.clock()
    
    def setScore(self, amount):
        self.score += amount
        
        #todo: gameover detection

    def update(self):
        lastupdate = time.clock()
        self.running = True
        while self.running:
            t = time.clock()
            dt = (t - lastupdate)
            lastupdate = t
            
            #print "update",dt,self.ball,self.ballvelocity * dt
            self.ball += self.ballvelocity * dt
            
            if self.ball.y > self.maxY:
                print "collision top",self.ball.y
                d = self.ball.y - self.maxY
                self.ball.y -= d
                self.ballvelocity.y *= -1
            elif self.ball.y < 0:
                print "collision bottom"
                self.ball.y = -self.ball.y
                self.ballvelocity.y *= -1
                
            if self.ball.x > self.maxX-1:
                if int(self.ball.y) == int(self.rightPaddle.y):
                    d = self.ball.x - (self.maxX-1)
                    self.ball.x -= d
                    self.ballvelocity.x *= -1
            elif self.ball.x < 1:
                if int(self.ball.y) == int(self.leftPaddle.y):
                    print "paddled!!!"
                    self.ball.x = 1 + self.ball.x
                    self.ballvelocity.x *= -1
                
            if self.ball.x > self.maxX:
                print "point for left"
                self.reset()
                self.setScore(-1)
            elif self.ball.x < 0:
                print "point for right"
                self.reset()
                self.setScore(1)
            #print self.ball
            
            self.ballspeed = 10 + (t - self.startTime)
            self.ballvelocity = self.ballvelocity.getNormalized() * self.ballspeed
            #print self.ballspeed
            
            self.draw()
            
            t2 = time.clock()
            time.sleep(1/30.0 - (t2-t))
    
    def draw(self):
        self.remote.clearPixels(self.grid, BLACK)
        
        self.remote.setPixel(self.grid, self.leftPaddle, BLUE)
        self.remote.setPixel(self.grid, self.rightPaddle, BLUE)
        self.remote.setPixel(self.grid, self.ball, WHITE)
        
        if self.score > 0:
            for i in range(self.score):
                if i > 5: break;
                self.remote.setPixel(self.grid, Vector(6+i,7), RED)
        else:
            for i in range(-self.score):
                if i > 5: break;
                self.remote.setPixel(self.grid, Vector(6-i,7), RED)
        
        self.remote.sendGrid(self.grid)

    def execute(self, data):
        result = False
        
        if not self.remote:
            self.init()
        
        print "pong - executing command:" + data['command']
        if data['command'] == 'pong_left_up':
            self.leftPaddle.y += 1
            if self.leftPaddle.y > self.maxY: self.leftPaddle.y = self.maxY
        elif data['command'] == 'pong_left_down':
            self.leftPaddle.y -= 1
            if self.leftPaddle.y < 0: self.leftPaddle.y = 0
        elif data['command'] == 'pong_right_up':
            self.rightPaddle.y += 1
            if self.rightPaddle.y > self.maxY: self.rightPaddle.y = self.maxY
        elif data['command'] == 'pong_right_down':
            self.rightPaddle.y -= 1
            if self.rightPaddle.y < 0: self.rightPaddle.y = 0
        
        self.draw()
        
        result = True
        
        return result


def getModule():
    return Pong()

