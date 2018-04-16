"""Rastrigin function GUI"""
import numpy as np

from si.gui import base


def rastrigin_fn(*X):
    return 10 * len(X) + sum([x ** 2 - 10 * np.cos(2 * np.pi * x) for x in X])


class RastriginFunctionGUI(base.FunctionGUI):
    def __init__(self):
        super(RastriginFunctionGUI, self).__init__(func=rastrigin_fn,
                                                   val_range=(-5.12, 5.12))
