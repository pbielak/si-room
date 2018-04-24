"""
Module for rastrigin function optimization problem
"""
import numpy as np


def rastrigin_fn(*X):
    return 10 * len(X) + sum([x ** 2 - 10 * np.cos(2 * np.pi * x) for x in X])
