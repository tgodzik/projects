import math
from pygame.locals import *
import pygame
import numpy as np
from .kalman import kalman_xy
from pymouse import PyMouse


mousi = PyMouse()
curx = -1
cury = -1
# add more in order to reach borders
delta = 100
res = [1680, 1050]
max_speed = [30, 30]
min_speed = [10, 10]


def move_mouse(center, width, height):
    # max 640
    #max 480

    global curx, cury
    x = center[0]
    y = center[1]

    wherex = (x / 640.0) * (res[0] + delta * 2)
    wherey = (y / 480.0) * (res[1] + delta * 2)

    if wherex > curx:
        difx = min(wherex - curx, max_speed[0])
    else:
        difx = - min(curx - wherex, max_speed[0])

    if abs(difx) < 5:
        difx = 0


    if wherey > cury:
        dify = min(wherey - cury, max_speed[1])
    else:
        dify = - min(cury - wherey, max_speed[1])

    if abs(dify) < 5:
        dify = 0

    #print curx, cury
    #difx, dify, _, _= predict_xy(difx, dify)
    curx += float(difx)
    cury += float(dify)
    mousi.move(min(max(0, curx - 100), res[0]), min(max(0, cury - 100), res[1]))


def set_mouse(x, y):
    global curx, cury
    curx = x
    cury = y
    newxy = predict_xy(x, y)
    mousi.move(newxy[0], newxy[1])


def click():
    pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN))


cur_x = np.matrix('5. 5. 0. 0.').T
p = np.matrix(np.eye(4)) * 100  # initial uncertainty
r = 0.1


def predict_xy(oldx, oldy):
    global cur_x, p, r
    cur_x, p = kalman_xy(cur_x, p, (oldx, oldy), r)
    return cur_x
