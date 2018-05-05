"""Rastrigin function GUI"""
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as patches
import numpy as np

from si.gui import base


class FunctionGUI(base.GUIWithSummaryPlot):
    def __init__(self, eval_fn, val_bounds, restricted):
        super(FunctionGUI, self).__init__(eval_fn)
        self.val_bounds = val_bounds
        self.restricted = restricted

        self.contour_ax = self.fig.add_subplot(121)
        self.marker_points = None

    def _draw(self):
        X = np.arange(self.val_bounds[0], self.val_bounds[1], 0.1)
        Y = np.arange(self.val_bounds[0], self.val_bounds[1], 0.1)

        X, Y = np.meshgrid(X, Y)

        Z = self.eval_fn((X, Y))

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

    def update_points(self, iteration, swarm, best_x):
        super(FunctionGUI, self).update_points(iteration, swarm, best_x)

        swarm_points = np.array(list(map(lambda ind: ind.x, swarm)))
        swarm_points = np.split(swarm_points, 2, axis=1)
        pts = (swarm_points[0].reshape(-1),
               swarm_points[1].reshape(-1))
        self.marker_points.set_data(pts)

        plt.pause(0.0001)
