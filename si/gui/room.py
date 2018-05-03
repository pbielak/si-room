import matplotlib.patches as patches
import matplotlib.pyplot as plt

from si.gui import base
from si.problem.room_planning import eval
from si.problem.room_planning import room as room_problem


class RoomGUI(base.GUI):

    def __init__(self, room):
        self.room = room

        self.avg_result_ax = None
        self.avg_results_x = []
        self.avg_results_y = []

        self._init_draw()

    def _init_draw(self):
        plt.ion()
        fig = plt.figure(figsize=(14, 7))
        self.room_ax = fig.add_subplot(121)
        self.color_map = plt.cm.get_cmap('hsv', 10)

        self.avg_result_ax = fig.add_subplot(122)

        self.avg_result_ax.set_title('Avg result')
        self.avg_result_ax.plot(0, 0)
        self.avg_result_ax.set_xlabel('Iteration')
        self.avg_result_ax.set_ylabel('Avg result')

    def draw(self):
        self._draw()
        plt.show()

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
        for idx, f in enumerate(sorted(self.room.furniture.values(), key=lambda x: type(x).__name__)):
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
            self.room_ax.text(f.figure.xmin, f.figure.ymin, type(f).__name__)

    def update_points(self, iteration, swarm, best_x):

        self.room = room_problem.solution_to_room(best_x, self.room)
        self._draw()

        eval_fn = lambda p: 1.0 / eval.evaluate_room(
                                room_problem.solution_to_room(p.x, self.room))
        avg_result = sum(map(eval_fn, swarm)) / len(swarm)
        self.avg_results_x.append(iteration)
        self.avg_results_y.append(avg_result)
        self.avg_result_ax.plot(self.avg_results_x,
                                self.avg_results_y,
                                color='g')

        plt.pause(0.0001)
