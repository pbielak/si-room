import matplotlib.pyplot as plt
import matplotlib.patches as patches

from si.gui.room_planning.room import Room, load_default_room_furniture


class RoomDrawer(object):

    def __init__(self):
        self._init_draw()

    def _init_draw(self):
        fig = plt.figure(figsize=(10, 10))
        self.room_ax = fig.add_subplot(111)

    def draw(self, room):
        self.room_ax.clear()

        self.room_ax.set_xlim(room.bounding_box.xmin, room.bounding_box.xmax)
        self.room_ax.set_ylim(room.bounding_box.ymin, room.bounding_box.ymax)

        # room walls
        self.room_ax.add_patch(patches.Rectangle(
            (room.bounding_box.xmin, room.bounding_box.ymin),
            room.bounding_box.width, room.bounding_box.height,
            linewidth=3, edgecolor='r', facecolor='none'))

        # carpet
        self.room_ax.add_patch(patches.Circle(
            (0, 0), room.carpet_radius,
            linewidth=1, edgecolor='g', facecolor='none'))

        # furniture
        for f in room.furniture:
            self.room_ax.add_patch(patches.Rectangle(
                (f.figure.xmin, f.figure.ymin),
                f.figure.width, f.figure.height,
                linewidth=1, edgecolor='b', facecolor='none'))

        plt.show()


# Test drawer
if __name__ == '__main__':
    r = Room(20, 20, load_default_room_furniture(), 3)
    rd = RoomDrawer()
    rd.draw(r)
