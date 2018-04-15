"""
Visualize function and update
"""
import matplotlib.pyplot as plt
import numpy as np

from si import visualization as gui


def main():
    rf = gui.RastriginFunctionGUI()
    rf.draw()
    for i in np.arange(-5.12, 5.12, 0.1):
        rf.update_points(([i, -1 * i], [i, -1 * i]))


if __name__ == '__main__':
    main()
    plt.show(block=True)
