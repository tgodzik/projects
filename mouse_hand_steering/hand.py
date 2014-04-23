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
# median_color = [(12, 96, 83), (15, 93, 77), (15, 99, 63), (13, 93, 77), (15, 90, 68), (18, 100, 67), (12, 86, 79)]
#median_color = [(12, 84, 71), (20, 82, 60), (19, 76, 51), (18, 90, 50), (13, 87, 48), (18, 82, 65), (18, 70, 48)]
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
    cv2.imshow("result", im)
    window.do()
    if cv2.waitKey(30) >= 113:
        pygame.quit()
        break


cv2.destroyAllWindows()
capture.release()


