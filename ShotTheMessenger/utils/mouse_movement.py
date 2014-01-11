from pymouse import PyMouse

mousi = PyMouse()
curx = 100
cury = 100
tempo = 10

def move_mouse(y, x, width, height):
    #print "Coordinates : ", x, y
    #print "Sizes : ", width, height
    global curx, cury
    #print x,y,width/3, height/3
    if x < width/3:
        curx -= tempo
    elif x > 2 * width/3:
        curx += tempo

    if y < height/3:
        cury -= tempo
    elif y > 2 * height/3:
        cury += tempo
    mousi.move(curx, cury)


def set_mouse(x, y):
    global curx, cury
    curx = x
    cury = y
    mousi.move(x, y)


def click():
    mousi.press(curx,cury)
