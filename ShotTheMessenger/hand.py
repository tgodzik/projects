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


capture = init_capture(1)

# try to measure the colors for the hand
init_windows(["img1"])
window = ButtonWindow((1200, 700))  # smaller
#window = ButtonWindow((1200, 900)) # bigger
window.do()
roi = wait_for_palm_cover(capture)
median_color = average(capture, roi)
# Get also size
print median_color
# median_color = [(167, 145, 16), (128, 151, 10), (120, 154, 5),
# (164, 141, 21), (173, 147, 38), (145, 144, 11), (161, 137, 25)]
median_color = [(13, 143, 23), (160, 149, 8), (120, 153, 9),
(158, 148, 10), (8, 128, 46), (144, 141, 14), (139, 139, 16)]
cv2.destroyWindow("img1")

init_windows(["result"])

retval, image = capture.read()

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
    im = analyse(bw, image)
    merge_image(im, bw)
    # what to show
    cv2.imshow("result", bw)
    window.do()
    if cv2.waitKey(30) >= 113:
        pygame.quit()
        break


cv2.destroyAllWindows()
capture.release()


