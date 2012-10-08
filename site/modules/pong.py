from ledlib.colors import *
from ledlib.remote import Remote
from vector import *

commands = ['pong_left_up', 'pong_left_down', 'pong_right_up', 'pong_right_down']
remote = None
grid = None

leftPaddle = Vector(0,4)
rightPaddle = Vector(11,4)
ball = Vector(6,4)

def init():
    remote = Remote()
    grid = remote.createGridBuffer(BLACK)
    remote.sendGrid(grid)

def execute(data):
    result = False

    if data['command'] == 'pong_left_up':
        pass
    elif data['command'] == 'pong_left_down':
        pass
    elif data['command'] == 'pong_right_up':
        pass
    elif data['command'] == 'pong_right_down':
        pass

    remote.clearPixels(grid, BLACK)
    
    remote.setPixel(grid, Vector(4,7), RED)
    remote.setPixel(grid, leftPaddle, BLUE)
    remote.setPixel(grid, rightPaddle, BLUE)
    remote.setPixel(grid, ball, WHITE)

    remote.sendGrid(grid)

    return result
