import cv2
from roi import Roi
import numpy as np


def markers(img):
    cols = len(img)
    rows = len(img[0])
    print img[cols / 3, rows / 6]
    print img[cols / 4, rows / 2]
    print img[cols / 3, rows / 1.5]
    print img[cols / 2, rows / 2]
    print img[cols / 2.5, rows / 2.5]
    print img[cols / 2, rows / 1.5]
    print img[cols / 2, rows / 1.8]


def wait_for_palm_cover(capture):
    retval, im = capture.read()
    square_len = 20
    roi = []
    #im = cv2.flip(im, 1)
    sh = im.shape
    cols = sh[0]
    rows = sh[1]
    roi.append(Roi((cols / 3, rows / 3.0), (cols / 3.0 + square_len, rows / 3.0 + square_len)))
    roi.append(Roi((cols / 4, rows / 2), (cols / 4 + square_len, rows / 2 + square_len)))
    roi.append(Roi((cols / 3, rows / 1.5), (cols / 3 + square_len, rows / 1.5 + square_len)))
    roi.append(Roi((cols / 2, rows / 2), (cols / 2 + square_len, rows / 2 + square_len)))
    roi.append(Roi((cols / 2.5, rows / 2.5), (cols / 2.5 + square_len, rows / 2.5 + square_len)))
    roi.append(Roi((cols / 2, rows / 1.5), (cols / 2 + square_len, rows / 1.5 + square_len)))
    roi.append(Roi((cols / 2.5, rows / 1.8), (cols / 2.5 + square_len, rows / 1.8 + square_len)))
    while cv2.waitKey(30) <= 0:
        retval, im = capture.read()
        #im = cv2.flip(im, 1)
        for j in range(0, len(roi)):
            roi[j].draw_rectangle(im)

        cv2.imshow("img1", im)
    return roi


def get_median(val):
    size = len(val)
    val.sort()
    if size % 2 == 0:
        median = val[size / 2 - 1]
    else:
        median = val[size / 2]

    return median


def get_median_color(roi, im):
    r = roi.get_region(im)
    hm = []
    sm = []
    lm = []
    cols = len(r)
    rows = len(r[0])
    for i in range(2, cols - 2):
        for j in range(2, rows - 2):
            hm.append(r[i][j][0])
            sm.append(r[i][j][1])
            lm.append(r[i][j][2])
    return get_median(hm), get_median(sm), get_median(lm)


def average(capture, roi):
    median_color = []
    retval, im = capture.read()
    #im = cv2.flip(im, 1)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
    for j in range(0, len(roi)):
        median_color.append(get_median_color(roi[j], im))
        roi[j].draw_rectangle(im)

    im = cv2.cvtColor(im, cv2.COLOR_HLS2BGR)
    cv2.imshow("img1", im)

    return median_color


def init_boundries(length):
    lower = []
    upper = []
    for i in range(0, length):
        lower.append((12, 30, 8))
        upper.append((7, 40, 30))
    return lower, upper


def produce_binaries(image, samples, avg_color):
    lower, upper = init_boundries(samples)
    masks = []
    for i in range(0, samples):
        lower_bound = np.array([max(0, avg_color[i][0] - lower[i][0]),
                                max(0, avg_color[i][1] - lower[i][1]), max(0, avg_color[i][2] - lower[i][2])])

        upper_bound = np.array([min(255, avg_color[i][0] + upper[i][0]),
                                min(255, avg_color[i][1] + upper[i][1]), min(255, avg_color[i][2] + upper[i][2])])
        #print "lower : ", lower_bound
        #print "upper :", upper_bound
        masks.append(cv2.inRange(image, lower_bound, upper_bound))
        #markers(image)
    mask = masks[0]
    for i in range(1, len(masks)):
        mask += masks[i]
    return cv2.medianBlur(mask, 7)


def find_biggest_contour(contours):
    biggest_size = -1
    biggest_contour = None
    for c in contours:
        if len(c) > biggest_size:
            biggest_size = len(c)
            biggest_contour = c
    return biggest_contour


def make_contours(bw):
    bw = cv2.pyrUp(bw)
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = find_biggest_contour(contours)
    if biggest is not None:
        bRect = cv2.boundingRect(biggest)
        hullP = cv2.convexHull(biggest)
        hullI = cv2.convexHull(biggest, returnPoints=False)
        hullP = cv2.approxPolyDP(hullP, 18, True)

        if len(biggest) > 3:
            defects = cv2.convexityDefects(biggest, hullI)
            # TODO hg->eleminateDefects(m);
        isHand = False #hg->detectIfHand();
        #hg->printGestureInfo(m->src);
        if isHand:
            pass #hg->getFingerTips(m);
            #hg->drawFingerTips(m);
            #myDrawContours(m,hg);


def simple_diff(image, previous_image, old_diff):
    import numpy as np

    if image is not None and previous_image is not None:
        tmp_image = image.astype(np.int)
        tmp_previous_image = previous_image.astype(np.int)
        diff = np.abs(tmp_image - tmp_previous_image)
        diff = diff.astype(np.uint8)
        diff = cv2.medianBlur(src=diff, ksize=11)
        diff = cv2.inRange(diff, np.array([20.0, 20.0, 20.0]), np.array([255.0, 255.0, 255.0]))
        measure = diff.sum() / (3 * 255.0)
        if measure > 500.0:
            return diff
        else:
            return old_diff