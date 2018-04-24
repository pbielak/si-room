"""Rastrigin function GUI"""
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as patches
import numpy as np

from si.gui import base


class FunctionGUI(base.GUI):
    def __init__(self, func, val_range, restricted):
        self.val_range = val_range
        self.eval_fn = func
        self.restricted = restricted

        self.contour_ax = None
        self.marker_points = None

        self.avg_result_ax = None
        self.avg_results_x = []
        self.avg_results_y = []

        self._setup()

    def _setup(self):
        plt.ion()
        fig = plt.figure(figsize=(14, 7))
        self.contour_ax = fig.add_subplot(121)
        self.avg_result_ax = fig.add_subplot(122)

    def draw(self):
        X = np.arange(self.val_range[0], self.val_range[1], 0.1)
        Y = np.arange(self.val_range[0], self.val_range[1], 0.1)

        X, Y = np.meshgrid(X, Y)

        Z = self.eval_fn(X, Y)

        self.contour_ax.contour(X, Y, Z, cmap=cm.coolwarm)

        if self.restricted:
            x = self.restricted
            self.contour_ax.add_patch(
                patches.Rectangle(xy=(-x, -x), width=2*x,
                                  height=2*x, fill=False)
            )

        self.marker_points = self.contour_ax.plot(1, 1, color='black',
                                                  marker='x', ms=10,
                                                  linestyle='')[0]

        self.avg_result_ax.set_title('Avg result')
        self.avg_result_ax.plot(0, 0)
        self.avg_result_ax.set_xlabel('Iteration')
        self.avg_result_ax.set_ylabel('Avg result')
        plt.show()

    def update_points(self, iteration, swarm, best_x):
        avg_result = sum(map(lambda p: self.eval_fn(*p.x), swarm)) / len(swarm)
        self.avg_results_x.append(iteration)
        self.avg_results_y.append(avg_result)
        self.avg_result_ax.plot(self.avg_results_x,
                                self.avg_results_y,
                                color='g')

        msg = 'Iteration: {} \n' \
              '(current best: {} => {})\n' \
              'Avg result: {}'.format(
            iteration, np.round(best_x, 2),
            np.round(self.eval_fn(best_x), 2),
            np.round(avg_result, 2)
        )
        self.contour_ax.set_title(msg)

        swarm_points = np.array(list(map(lambda ind: ind.x, swarm)))
        swarm_points = np.split(swarm_points, 2, axis=1)
        pts = (swarm_points[0].reshape(-1),
               swarm_points[1].reshape(-1))
        self.marker_points.set_data(pts)

        plt.pause(0.0001)
