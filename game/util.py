import math

class Point:
    def __init__(self, *args, pos=None):
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif pos is not None:
            self.x, self.y = pos
        else:
            raise ValueError("Error in point initialization")

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)

    def distance_to(self, o):
        return math.sqrt((self.x - o.x) ** 2 + (self.y - o.y) ** 2)

    def length(self):
        origo = Point(0, 0)
        return self.distance_to(origo)

    def multiply(self, factor):
        return Point(self.x*factor, self.y*factor)

    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)
