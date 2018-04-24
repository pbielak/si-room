"""
Module for room class and functions
"""
import numpy as np

from si.gui.room_planning import furniture as fun
from si.gui.room_planning import geometry as geom


class Room(object):
    def __init__(self, width, height, furniture_classes, carpet_radius):
        self.bounding_box = geom.Rectangle(0, 0, width, height)
        self.furniture = self._init_furniture(furniture_classes)
        self.carpet_radius = carpet_radius

    def _init_furniture(self, furniture_classes):
        furniture = []
        for cls in furniture_classes:
            x = np.random.uniform(self.bounding_box.xmin,
                                  self.bounding_box.xmax)
            y = np.random.uniform(self.bounding_box.ymin,
                                  self.bounding_box.ymax)

            f = cls(x, y)
            if not geom.inside(f.figure, self.bounding_box):
                geom.move_inside(f.figure, self.bounding_box)

            furniture.append(f)
        return furniture


def load_default_room_furniture():
    furniture_classes = [
        fun.Wardrobe,
        fun.Table,
        fun.Sofa
        # ...
    ]
    return furniture_classes
