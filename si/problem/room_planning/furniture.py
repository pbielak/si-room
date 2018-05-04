"""
Module for furniture definition
"""
from si.problem.room_planning import geometry as geom

WINDOW_WIDTH = 2
DOOR_HEIGHT = 4


class Furniture(object):
    def __init__(self, x, y, width, height, carpet):
        self.figure = geom.Rectangle(x, y, width, height)
        self.carpet = carpet

    def __repr__(self):
        return "{}[pos=({}, {}), size=({}, {}), {}]".format(
            self.__class__.__name__,
            self.figure.x, self.figure.y,
            self.figure.width, self.figure.height,
            self.carpet
        )


class Wardrobe(Furniture):
    def __init__(self, x, y):
        super(Wardrobe, self).__init__(x, y, width=5, height=10, carpet=False)


class Table(Furniture):
    def __init__(self, x, y):
        super(Table, self).__init__(x, y, width=10, height=10, carpet=True)


class Sofa(Furniture):
    def __init__(self, x, y):
        super(Sofa, self).__init__(x, y, width=15, height=4, carpet=True)


class TV(Furniture):
    def __init__(self, x, y):
        super(TV, self).__init__(x, y, width=5, height=2, carpet=False)


class Desk(Furniture):
    def __init__(self, x, y):
        super(Desk, self).__init__(x, y, width=7, height=13, carpet=False)


class Chair(Furniture):
    def __init__(self, x, y):
        super(Chair, self).__init__(x, y, width=2.5, height=2.5, carpet=True)


class Window(Furniture):
    def __init__(self, x, y):
        super(Window, self).__init__(x, y, width=WINDOW_WIDTH, height=10, carpet=True)


class Door(Furniture):
    def __init__(self, x, y):
        super(Door, self).__init__(x, y, width=8, height=DOOR_HEIGHT, carpet=True)
