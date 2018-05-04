"""
Module for room class and functions
"""
import numpy as np
from copy import deepcopy

from si.problem.room_planning import furniture as fun, geometry as geom
from si.problem.room_planning.furniture import WINDOW_WIDTH, DOOR_HEIGHT


class Room(object):
    def __init__(self, width, height, furniture_classes=None):
        self.bounding_box = geom.Rectangle(0, 0, width, height)
        self.carpet_radius = None

        if furniture_classes is None:
            furniture_classes = load_default_room_furniture()

        self.furniture = self._init_furniture(furniture_classes)
        self.update_carpet_size()

    def _init_furniture(self, furniture_classes):
        furniture = {}
        for f_name, f_cls in furniture_classes.items():

            if f_name == 'Window' or f_name == 'Door':
                continue

            x = np.random.uniform(self.bounding_box.xmin,
                                  self.bounding_box.xmax)
            y = np.random.uniform(self.bounding_box.ymin,
                                  self.bounding_box.ymax)

            f = f_cls(x, y)
            if not geom.inside(f.figure, self.bounding_box):
                geom.move_inside(f.figure, self.bounding_box)

            furniture[f_name] = f

        # setup door and window positions
        furniture['Window'] = fun.Window(
            -self.bounding_box.width / 2 + WINDOW_WIDTH / 2, 0)
        furniture['Door'] = fun.Door(
            0, self.bounding_box.height / 2 - DOOR_HEIGHT / 2)

        return furniture

    def update_carpet_size(self):
        furniture = list(map(lambda x: x.figure,
                             filter(lambda x: not x.carpet,
                                    self.furniture.values())))

        carpet_radius = min(self.bounding_box.width / 2,
                            self.bounding_box.height / 2)

        while carpet_radius > 0:
            carpet_box = geom.Rectangle(0, 0,
                                        carpet_radius * 2,
                                        carpet_radius * 2)

            found_intersecting_furniture = False

            for f in furniture:
                if geom.intersects(f, carpet_box):
                    found_intersecting_furniture = True
                    break

            if found_intersecting_furniture:
                carpet_radius -= 0.5
            else:
                break

        assert carpet_radius >= 0
        self.carpet_radius = carpet_radius


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
        'Desk': fun.Desk,
        'Window': fun.Window,
        'Door': fun.Door,
    }
    return furniture_classes


def solution_to_room(solution, old_room):
    room = deepcopy(old_room)

    f = room.furniture

    f['Wardrobe1'].figure.x = solution[0]
    f['Wardrobe1'].figure.y = solution[1]

    f['Wardrobe2'].figure.x = solution[2]
    f['Wardrobe2'].figure.y = solution[3]

    f['TV'].figure.x = solution[4]
    f['TV'].figure.y = solution[5]

    f['Sofa'].figure.x = solution[6]
    f['Sofa'].figure.y = solution[7]

    f['Table'].figure.x = solution[8]
    f['Table'].figure.y = solution[9]

    f['Chair1'].figure.x = solution[10]
    f['Chair1'].figure.y = solution[11]

    f['Chair2'].figure.x = solution[12]
    f['Chair2'].figure.y = solution[13]

    f['Chair3'].figure.x = solution[14]
    f['Chair3'].figure.y = solution[15]

    f['Chair4'].figure.x = solution[11]
    f['Chair4'].figure.y = solution[17]

    f['Desk'].figure.x = solution[18]
    f['Desk'].figure.y = solution[19]

    room.update_carpet_size()
    return room
