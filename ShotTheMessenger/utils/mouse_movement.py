from pymouse import PyMouse
import math
mousi = PyMouse()
curx = -1
cury = -1
res = [1680, 1050]
tempo = 10
tolerance = [20, 200]


def move_mouse(center, width, height):
    # max 640
    x = center[0]
    #max 480
    y = center[1]

    #print "Coordinates : ", x, y
    #print "Sizes : ", width, height
    global curx, cury
    oldx, oldy = curx, cury
    curx = (x/640.0) * res[0]
    cury = (y/480.0) * res[1]
    dist = math.sqrt(math.pow(oldx-curx, 2) + math.pow(oldy-cury, 2))
     # possible to add delta in order to reach more
    if tolerance[0] < dist < tolerance[1] or (oldx == -1 and oldy == -1):
        mousi.move(curx, cury)
    else:
        curx, cury = oldx, oldy


def set_mouse(x, y):
    global curx, cury
    curx = x
    cury = y
    mousi.move(x, y)


def click():
    mousi.press(curx, cury)
