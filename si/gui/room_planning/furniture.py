"""
Module for furniture definition
"""
from si.gui.room_planning import geometry as geom


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
        super(Table, self).__init__(x, y, width=1.5, height=1.5, carpet=True)


class Sofa(Furniture):
    def __init__(self, x, y):
        super(Sofa, self).__init__(x, y, width=5, height=3, carpet=False)

# TODO: define rest of furniture
