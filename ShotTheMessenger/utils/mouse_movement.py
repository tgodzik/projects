from pymouse import PyMouse
import math
from pygame.locals import *

import  pygame
mousi = PyMouse()
curx = -1
cury = -1
# add more in order to reach borders
delta = 100
res = [1680, 1050]
tempo = 10
tolerance = [30, 250]


def move_mouse(center, width, height):
    # max 640
    x = center[0]
    #max 480
    y = center[1]

    #print "Coordinates : ", x, y
    #print "Sizes : ", width, height
    global curx, cury
    oldx, oldy = curx, cury
    curx = (x/640.0) * (res[0] + delta * 2)
    cury = (y/480.0) * (res[1] + delta * 2)
    dist = math.sqrt(math.pow(oldx-curx, 2) + math.pow(oldy-cury, 2))
     # possible to add delta in order to reach more
    if tolerance[0] < dist < tolerance[1] or (oldx == -1 and oldy == -1):
        mousi.move(min(max(0, curx-100), res[0]), min(max(0, cury-100), res[1]))
    else:
        curx, cury = oldx, oldy


def set_mouse(x, y):
    global curx, cury
    curx = x
    cury = y
    mousi.move(x, y)


def click():
    pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN))
