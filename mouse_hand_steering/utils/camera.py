import cv2
import sys


def init_capture(which_camera):
    """
    starts the camera capture
    """
    capture = cv2.VideoCapture(which_camera)
    if not capture:
        print "Error initializing capture"
        sys.exit(0)
    return capture


def init_windows(names):
    """
    Creates the windows with names.
    """
    for name in names:
        cv2.namedWindow(name, cv2.CV_WINDOW_AUTOSIZE)


def merge_image(im, bw):
    """
    Merge the black and white image into the large color image.
    """
    bw = cv2.pyrDown(bw)
    bw = cv2.pyrDown(bw)
    newbw = cv2.merge([bw, bw, bw])
    sh = newbw.shape
    x = sh[0]
    y = sh[1]
    im[0:x, 0:y] = newbw