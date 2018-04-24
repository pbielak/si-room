"""
Module for geometric functions stuff
"""


class Rectangle(object):
    def __init__(self, x, y, width, height):
        """(x, y) is the center of the rectangle"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def xmin(self):
        return self.x - self.width / 2.0

    @property
    def xmax(self):
        return self.x + self.width / 2.0

    @property
    def ymin(self):
        return self.y - self.height / 2.0

    @property
    def ymax(self):
        return self.y + self.height / 2.0


def inside(r_inner, r_outer):
    return r_inner.xmax < r_outer.xmax and r_inner.xmin > r_outer.xmin and \
           r_inner.ymax < r_outer.ymax and r_inner.ymin > r_outer.ymin


def move_inside(r, r_outer):
    # On X-axis
    if r.xmin < r_outer.xmin:  # Needs to be shifted right
        r.x += r_outer.xmin - r.xmin
    elif r.xmax > r_outer.xmax:  # Needs to be shifted left
        r.x -= r.xmax - r_outer.xmax

    # On Y-axis
    if r.ymin < r_outer.ymin:  # Needs to be shifted up
        r.y += r_outer.ymin - r.ymin
    elif r.ymax > r_outer.ymax:  # Needs to be shifted down
        r.y -= r.ymax - r_outer.ymax


def intersects(r1, r2):
    return overlapping_area(r1, r2) > 0


def overlapping_area(r1, r2):
    dx = min(r1.xmax, r2.xmax) - max(r1.xmin, r2.xmin)
    dy = min(r1.ymax, r2.ymax) - max(r1.ymin, r2.ymin)
    if dx > 0 and dy > 0:
        return dx * dy

    return 0


def flip(r):
    r.x, r.y = r.y, r.x
    r.width, r.height = r.height, r.width


def distance(r1, r2):
    # TODO: need to calc distance between two items
    return 42


def angle(r1, r2):
    # TODO: need to calc angle between two items
    return 42
