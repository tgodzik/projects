import cv2
import sys


def init_capture(which_camera):
        capture = cv2.VideoCapture(which_camera)
        if not capture:
                print "Error initializing capture"
                sys.exit(0)
        return capture


def init_windows(names):
        for name in names:
            cv2.namedWindow(name, cv2.CV_WINDOW_AUTOSIZE)