"""
Bat Algorithm
"""
from collections import namedtuple

import numpy as np

from si.algorithm import base
from si import utils


class Bat(base.Individual):
    def __init__(self, x, v, f, r, A):
        super(Bat, self).__init__(x)
        self.v = v
        self.f = f
        self.r = r
        self.A = A
        self.t = 1

    def get_best(self):
        return self.x

    def __repr__(self):
        return "B(pos={}, vel={}, freq={}, rate={}, loud={})".format(
            self.x, self.v, self.f, self.r, self.A
        )


BatOptions = namedtuple('BatOptions', ['alpha', 'gamma', 'f_min', 'f_max',
                                       'A_0', 'A_min'])


class BatAlgorithm(base.SwarmIntelligenceAlgorithm):
    def __init__(self, eval_fn, update_gui_callback,
                 swarm_size, val_bounds, nb_dim, options):
        super(BatAlgorithm, self).__init__(eval_fn, update_gui_callback,
                                           swarm_size, val_bounds,
                                           nb_dim, options)

    def get_random_individual(self):
        min_val, max_val = self.val_bounds

        x = utils.uniform(min_val, max_val, self.nb_dim)
        v = utils.uniform(min_val, max_val, self.nb_dim)
        f = utils.uniform(self.options.f_min, self.options.f_max, 1)
        r = utils.uniform(0, 1, 1)
        A = utils.uniform(self.options.A_min, self.options.A_0, 1)

        return Bat(x, v, f, r, A)

    def update_individual(self, ind):
        ind.f = self.options.f_min + \
                (self.options.f_max - self.options.f_min) * \
                utils.uniform(0, 1, 1)
        ind.v = ind.v + (self.best_x - ind.x) * ind.f
        ind.x = ind.x + ind.v

        x = ind.x

        if utils.uniform(0, 1, 1) > ind.r:
            x = self.best_x + utils.uniform(-1, 1, self.nb_dim) * \
                              self._avg_loudness() * 1e-6

        x += 1e-6 * utils.uniform(-1, 1, self.nb_dim)

        if utils.uniform(0, 1, 1) < ind.A \
            and self.eval_fn(*x) < self.eval_fn(*self.best_x):
            ind.x = x

        ind.A = max(self.options.A_min, self.options.alpha * ind.A)
        ind.r = 0.01 * (1 - np.exp((-1) * self.options.gamma * ind.t))
        ind.t += 1

    def _avg_loudness(self):
        return sum(map(lambda ind: ind.A, self.individuals)) / self.swarm_size
