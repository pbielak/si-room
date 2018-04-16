"""
Base classes for GUI
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


class GUI(object):
    def draw(self):
        pass

    def update_points(self, msg, pts, avg_result):
        pass


class FunctionGUI(GUI):
    def __init__(self, func, val_range):
        self.val_range = val_range
        self.fn = func
        self.surface_ax = None

        self.contour_ax = None
        self.marker_points = None

        self.avg_result_ax = None
        self.avg_results_x = []
        self.avg_results_y = []

        self._setup()

    def _setup(self):
        plt.ion()
        fig = plt.figure(figsize=(14, 7))
        self.surface_ax = fig.add_subplot(221, projection='3d')
        self.contour_ax = fig.add_subplot(222)
        self.avg_result_ax = fig.add_subplot(223)

    def draw(self):
        X = np.arange(self.val_range[0], self.val_range[1], 0.1)
        Y = np.arange(self.val_range[0], self.val_range[1], 0.1)

        X, Y = np.meshgrid(X, Y)

        Z = self.fn(X, Y)

        self.surface_ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                                     linewidth=0, antialiased=False)

        self.contour_ax.contour(X, Y, Z, cmap=cm.coolwarm)

        self.marker_points = self.contour_ax.plot(1, 1, color='black',
                                                  marker='x', ms=10,
                                                  linestyle='')[0]

        self.avg_result_ax.set_title('Avg result')
        self.avg_result_ax.plot(0, 0)
        self.avg_result_ax.set_xlabel('Iteration')
        self.avg_result_ax.set_ylabel('Avg result')
        plt.show()

    def update_points(self, msg, pts, avg_result):
        self.contour_ax.set_title(msg)
        self.marker_points.set_data(pts)

        self.avg_results_x.append(avg_result[0])
        self.avg_results_y.append(avg_result[1])
        self.avg_result_ax.plot(self.avg_results_x,
                                self.avg_results_y,
                                color='g')
        plt.pause(0.0001)
