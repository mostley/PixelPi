from ledlib.colors import *
from ledlib.remote import Remote
from ledlib.vector import *

class Pong:
    def __init__(self):
        self.commands = ['pong_left_up', 'pong_left_down', 'pong_right_up', 'pong_right_down']
        self.remote = None
        self.grid = None
        self.leftPaddle = Vector(0,4)
        self.rightPaddle = Vector(11,4)
        self.ball = Vector(6,4)

    def init(self):
        self.remote = Remote()
        self.grid = self.remote.createGridBuffer(BLACK)
        self.remote.sendGrid(self.grid)

    def execute(self, data):
        result = False
        
        if not self.remote:
            self.init()
        
        if data['command'] == 'pong_left_up':
            self.leftPaddle.y += 1
        elif data['command'] == 'pong_left_down':
            self.leftPaddle.y -= 1
        elif data['command'] == 'pong_right_up':
            self.rightPaddle.y += 1
        elif data['command'] == 'pong_right_down':
            self.rightPaddle.y -= 1
        
        self.remote.clearPixels(self.grid, BLACK)
        
        #self.remote.setPixel(self.grid, Vector(4,7), RED)
        self.remote.setPixel(self.grid, self.leftPaddle, BLUE)
        self.remote.setPixel(self.grid, self.rightPaddle, BLUE)
        self.remote.setPixel(self.grid, self.ball, WHITE)
        
        self.remote.sendGrid(self.grid)
        
        return result


def getModule():
    return Pong()

