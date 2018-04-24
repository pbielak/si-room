"""
Module for room class and functions
"""
import numpy as np

from si.problem.room_planning import furniture as fun, geometry as geom


class Room(object):
    def __init__(self, width, height, furniture_classes, carpet_radius):
        self.bounding_box = geom.Rectangle(0, 0, width, height)
        self.furniture = self._init_furniture(furniture_classes)
        self.carpet_radius = carpet_radius

    def _init_furniture(self, furniture_classes):
        furniture = {}
        for f_name, f_cls in furniture_classes.items():
            x = np.random.uniform(self.bounding_box.xmin,
                                  self.bounding_box.xmax)
            y = np.random.uniform(self.bounding_box.ymin,
                                  self.bounding_box.ymax)

            f = f_cls(x, y)
            if not geom.inside(f.figure, self.bounding_box):
                geom.move_inside(f.figure, self.bounding_box)

            furniture[f_name] = f
        return furniture


def load_default_room_furniture():
    furniture_classes = {
        'Wardrobe1': fun.Wardrobe,
        'Wardrobe2': fun.Wardrobe,
        'TV': fun.TV,
        'Sofa': fun.Sofa,
        'Table': fun.Table,
        'Chair1': fun.Chair,
        'Chair2': fun.Chair,
        'Chair3': fun.Chair,
        'Chair4': fun.Chair,
        'Desk': fun.Desk
    }
    return furniture_classes
