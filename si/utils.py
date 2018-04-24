"""
Module for util functions
"""
import numpy as np


def uniform(min_val=0, max_val=1, size=2):
    return np.random.uniform(min_val, max_val, size)
