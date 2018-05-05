import matplotlib.patches as patches
import matplotlib.pyplot as plt

from si.gui import base
from si.problem.room_planning import room as room_problem


class RoomGUI(base.GUIWithSummaryPlot):

    def __init__(self, room, eval_fn):
        super(RoomGUI, self).__init__(eval_fn)
        self.room = room
        self.room_ax = self.fig.add_subplot(121)
        self.color_map = plt.cm.get_cmap('hsv', 12)

    def _draw(self):
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
        for idx, f in enumerate(sorted(self.room.furniture.values(),
                                       key=lambda x: type(x).__name__)):
            if type(f).__name__ in ('Window', 'Door'):
                patch_kwargs = dict(
                    linewidth=1,
                    hatch='\\',
                    fill=False
                )
            else:
                patch_kwargs = dict(
                    linewidth=1,
                    color=self.color_map(idx),
                    alpha=0.8
                )

            fg = f.figure
            self.room_ax.add_patch(
                patches.Rectangle(
                    (fg.xmin, fg.ymin),
                    fg.width,
                    fg.height,
                    **patch_kwargs
                )
            )
            self.room_ax.text(f.figure.xmin, f.figure.ymin, type(f).__name__)

    def update_points(self, iteration, swarm, best_x):
        super(RoomGUI, self).update_points(iteration, swarm, best_x)

        self.room = room_problem.solution_to_room(best_x, self.room)
        self._draw()

        plt.pause(0.0001)
