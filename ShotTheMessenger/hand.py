__author__ = 'Tomasz Godzik'
'''
 Simple hand detection algorithm made with OpenCV

 Based on C++ program in github.com/simena86/handDetectionCV
 Using python allows for fast prototyping.
'''
import cv2
from utils import *
from interface import *
import pygame

#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9), (4, 4))

capture = init_capture(1)

# try to measure the colors for the hand
init_windows(["img1"])
window = ButtonWindow((1200, 900))
window.do()
roi = wait_for_palm_cover(capture)
median_color = average(capture, roi)
# Get also size
print median_color
cv2.destroyWindow("img1")

init_windows(["result"])

#k = cv2.waitKey(10)
retval, image = capture.read()
#set_mouse(100, 100)

while True:
    oldimage = image
    retval, image = capture.read()
    #to_analize = image/2 + oldimage/2
    #image = cv2.flip(image,1)
    imLR = cv2.pyrDown(image)
    imLR = cv2.blur(imLR, (3, 3))
    imLR = cv2.cvtColor(imLR, cv2.COLOR_BGR2HLS)
    bw = produce_binaries(imLR, len(roi), median_color)
    imLR = cv2.cvtColor(imLR, cv2.COLOR_HLS2BGR)
    im = make_contours(bw, image)
    merge_image(im, bw)
    cv2.imshow("result", im)
    window.do()
    if cv2.waitKey(30) >= 113:
        pygame.quit()
        break


cv2.destroyAllWindows()
capture.release()


