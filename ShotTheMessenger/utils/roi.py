import cv2
import numpy


class Roi:
    def __init__(self, lcorner=(0, 0), ucorner=(0, 0)):
        self.upper_corner = int(ucorner[0]), int(ucorner[1])
        self.lower_corner = int(lcorner[0]), int(lcorner[1])
        self.color = (0, 255, 0)
        self.border_thickness = 2

    def draw_rectangle(self, src):
        cv2.rectangle(src,  (self.upper_corner[1], self.upper_corner[0]), (self.lower_corner[1], self.lower_corner[0]),
                      self.color, self.border_thickness)

    def get_region(self, image):
        return image[self.lower_corner[0]:self.upper_corner[0],self.lower_corner[1]:self.upper_corner[1]]