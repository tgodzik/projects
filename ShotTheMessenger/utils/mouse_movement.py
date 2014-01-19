from pygame.locals import *
import pygame
from pymouse import PyMouse
import cv2.cv as cv

# init mouse and kalman filter
mousi = PyMouse()
curx = -1
cury = -1

delta = 100
#res = [1680, 1050]
res = [1366, 768]
max_speed = [30, 30]
min_speed = [10, 10]

rng = cv.RNG(-1)
kalman = cv.CreateKalman(4, 2, 0)

kalman.transition_matrix[0, 0] = 1
kalman.transition_matrix[0, 1] = 0
kalman.transition_matrix[0, 2] = 1
kalman.transition_matrix[0, 3] = 0

kalman.transition_matrix[1, 0] = 0
kalman.transition_matrix[1, 1] = 1
kalman.transition_matrix[1, 2] = 0
kalman.transition_matrix[1, 3] = 1

kalman.transition_matrix[2, 0] = 0
kalman.transition_matrix[2, 1] = 0
kalman.transition_matrix[2, 2] = 1
kalman.transition_matrix[2, 3] = 0

kalman.transition_matrix[3, 0] = 0
kalman.transition_matrix[3, 1] = 0
kalman.transition_matrix[3, 2] = 0
kalman.transition_matrix[3, 3] = 1

kalman.state_pre[0, 0] = 5
kalman.state_pre[1, 0] = 5
kalman.state_pre[2, 0] = 0
kalman.state_pre[3, 0] = 0

cv.SetIdentity(kalman.measurement_matrix, cv.RealScalar(1))
cv.SetIdentity(kalman.process_noise_cov, cv.RealScalar(1e-4))
cv.SetIdentity(kalman.measurement_noise_cov, cv.RealScalar(1e-1))
cv.SetIdentity(kalman.error_cov_post, cv.RealScalar(.1))


def move_mouse(center, width, height):
    """
    Move mouse to a point with kalman filter and scaling.
    """
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

    pred = cv.KalmanPredict(kalman)
    measurement = cv.CreateMat(2, 1, cv.CV_32FC1)
    measurement[0, 0] = difx
    measurement[1, 0] = dify
    estimated = cv.KalmanCorrect(kalman, measurement)
    difx, dify = estimated[0, 0], estimated[1, 0]
    curx += float(difx)
    cury += float(dify)
    mousi.move(min(max(0, curx - 100), res[0]), min(max(0, cury - 100), res[1]))


def set_mouse(x, y):
    """
    Move mouse.
    """
    mousi.move(x, y)


def click():
    """
    Click mouse.
    """
    pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN))


