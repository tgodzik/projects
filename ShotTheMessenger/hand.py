__author__ = 'Tomasz Godzik'
'''
 Simple hand detection algorithm based on OpenCV

 Based on https://github.com/bengal/opencv-hand-detection

'''

import cv2
import numpy as np
import sys

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9), (4, 4))


def init_capture():
        capture = cv2.VideoCapture(0)
        if not capture:
                print "Error initializing capture"
                sys.exit(0)
        return capture


#def init_recording(ctx):
#
#        ctx.writer = cv2.VideoWriter()
#
#        if not ctx.writer:
#                print "Error initializing video writer"
#                sys.exit(1)


def init_windows():
        cv2.namedWindow("output", cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow("thresholded", cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow("diff", cv2.CV_WINDOW_AUTOSIZE)


def filter_and_threshold(picture):
    # Soften image
    tmp_image = cv2.GaussianBlur(src=picture, ksize=(11, 11), sigmaX=0, sigmaY=0)

    # Remove some impulsive noise
    tmp_image = cv2.medianBlur(src=tmp_image, ksize=11)

    tmp_image = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2HSV)

    # Apply threshold on HSV values to detect skin color
    tmp_image = cv2.inRange(tmp_image, np.array([0.0, 55.0, 90.0, 255.0]), np.array([28.0, 175.0, 230.0, 255.0]))

    # Apply morphological opening
    tmp_image = cv2.morphologyEx(tmp_image, cv2.MORPH_OPEN, kernel)

    tmp_image = cv2.GaussianBlur(src=tmp_image, ksize=(3, 3), sigmaX=0, sigmaY=0)

    return tmp_image


def simple_diff(image, previous_image, old_diff):
    if image is not None and previous_image is not None:
        tmp_image = image.astype(np.int)
        tmp_previous_image = previous_image.astype(np.int)
        diff = np.abs(tmp_image - tmp_previous_image )
        diff = diff.astype(np.uint8)
        diff = cv2.medianBlur(src=diff, ksize=11)
        diff = cv2.inRange(diff, np.array([20.0, 20.0, 20.0]), np.array([255.0, 255.0, 255.0]))
        measure = diff.sum()/(3*255.0)
        if measure > 500.0:
            return diff
        else:
            return old_diff


#def main():
#        init_capture(context)
#        init_windows()
#        ret, context.image = context.capture.read();
#
#        k = cv2.waitKey(10)
#        while k != 113:
#
#            context.previous_image = context.image
#
#            ret, context.image = context.capture.read()
#
#            simple_diff(context)
#            filter_and_threshold(context)
#
#            #find_contour(&ctx);
#            #find_convex_hull(&ctx);
#            #find_fingers(&ctx);
#            #display(&ctx);
#            cv2.imshow("output", context.image)
#            cv2.imshow("thresholded", context.thresholded)
#            if context.diff_image is not None:
#                cv2.imshow("diff", context.diff_image)
#            #ctx.writer.write(ctx.image)
#            k = cv2.waitKey(10)


capture = init_capture()

init_windows()

ret, image = capture.read()
previous_image = image
diff = image

k = cv2.waitKey(10)
while k != 113:

            previous_image = image
            ret, image = capture.read()

            diff = simple_diff(image, previous_image, diff)
            thresholded = filter_and_threshold(image)
            #cv2.convexityDefects(None, None)
            #find_contour(&ctx);
            #find_convex_hull(&ctx);
            #find_fingers(&ctx);
            #display(&ctx);
            cv2.imshow("output", image)
            cv2.imshow("thresholded", thresholded)
            cv2.imshow("diff", diff)
            #ctx.writer.write(ctx.image)
            k = cv2.waitKey(10)

