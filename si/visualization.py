"""Visualizations"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


class GUI(object):
    def draw(self):
        pass

    def update_points(self, pts):
        pass


class RastriginFunctionGUI(GUI):
    def __init__(self):
        self.surface_ax = None
        self.contour_ax = None
        self.marker_points = None
        self._setup()

    def _setup(self):
        plt.ion()
        fig = plt.figure()
        self.surface_ax = fig.add_subplot(121, projection='3d')
        self.contour_ax = fig.add_subplot(122)

    def _rastrigin_fn(self, *X):
        return 10 * len(X) + sum([x ** 2 - 10 * np.cos(2 * np.pi * x) for x in X])

    def draw(self):
        X = np.arange(-5.12, 5.12, 0.1)
        Y = np.arange(-5.12, 5.12, 0.1)

        X, Y = np.meshgrid(X, Y)

        Z = self._rastrigin_fn(X, Y)

        self.surface_ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                                     linewidth=0, antialiased=False)

        self.contour_ax.contour(X, Y, Z, cmap=cm.coolwarm)

        self.marker_points = self.contour_ax.plot(1, 1, color='black',
                                                  marker='x', linestyle='')[0]
        plt.show()

    def update_points(self, pts):
        self.marker_points.set_data(pts)
        plt.pause(0.0001)
