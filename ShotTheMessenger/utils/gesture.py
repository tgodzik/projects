import math


def distance(point1, point2):
    point1 = point1[0]
    point2 = point2[0]
    return math.sqrt(math.pow(point1[0]-point2[0], 2) + math.pow(point1[1]-point2[1], 2))


class Gesture:

    def __init__(self):
        self.hull_p = None
        self.hull_i = None
        self.biggest = None
        self.bounding = None
        self.defects = None
        self.contours = None

    def check_convexity(self, m):
        tolerance = (self.bounding[0] - self.bounding[2])/5
        angleTol = 95.0
        new_defects = []

        if self.defects is not None:
            for i in self.defects:
                j = i[0]
                start = self.contours[self.biggest][j[1]]
                end = self.contours[self.biggest][j[0]]
                far = self.contours[self.biggest][j[2]]
                if distance(start, far) > tolerance and distance (end, far)>tolerance:
                    new_defects.append(i)

        self.defects = new_defects

    def is_hand(self):
        h = self.bounding[0] - self.bounding[2]
        w = self.bounding[1] - self.bounding[3]
        hand = True
        if h is 0 or w is 0:
            hand = False
        elif h/w > 4 or w/h > 4:
            hand = False
        return hand