import matplotlib.patches as patches
import matplotlib.pyplot as plt

from si.gui import base
from si.problem.room_planning.eval import evaluate_room
from si.problem.room_planning.room import Room, load_default_room_furniture


class RoomGUI(base.GUI):

    def __init__(self, room):
        self.room = room
        self._init_draw()

    def _init_draw(self):
        fig = plt.figure(figsize=(7, 7))
        self.room_ax = fig.add_subplot(111)
        self.color_map = plt.cm.get_cmap('hsv', 10)

    def draw(self):
        self.room_ax.clear()

        room_bb = self.room.bounding_box

        self.room_ax.set_xlim(room_bb.xmin, room_bb.xmax)
        self.room_ax.set_ylim(room_bb.ymin, room_bb.ymax)

        # room walls
        self.room_ax.add_patch(
            patches.Rectangle(
                (room_bb.xmin, room_bb.ymin),
                room_bb.width,
                room_bb.height,
                linewidth=3,
                color='grey'
            )
        )

        # carpet
        self.room_ax.add_patch(
            patches.Circle(
                (0, 0),
                self.room.carpet_radius,
                linewidth=1,
                color='chocolate',
                alpha=0.5,
                hatch='*'
            )
        )

        # furniture
        for idx, f in enumerate(self.room.furniture.values()):
            fg = f.figure
            self.room_ax.add_patch(
                patches.Rectangle(
                    (fg.xmin, fg.ymin),
                    fg.width,
                    fg.height,
                    linewidth=1,
                    color=self.color_map(idx),
                    alpha=0.8
                )
            )
            plt.text(f.figure.xmin, f.figure.ymin, type(f).__name__)

        plt.show()

    def update_points(self, iteration, swarm, best_x):
        (w1x, w1y, w2x, w2y, tvx, tvy, sx, sy, tx, ty,
         c1x, c1y, c2x, c2y, c3x, c3y, c4x, c4y, dx, dy) = best_x


# Test drawer and evaluator
if __name__ == '__main__':
    r = Room(40, 40, 3, furniture_classes=load_default_room_furniture())
    print(evaluate_room(r))
    rd = RoomGUI(r)
    rd.draw()
