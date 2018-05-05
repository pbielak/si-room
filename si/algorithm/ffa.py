"""
Firefly algorithm
"""
from collections import namedtuple

import numpy as np

from si.algorithm import base
from si import utils


class Firefly(base.Individual):
    def __init__(self, x):
        super(Firefly, self).__init__(x)

    def get_best(self):
        return self.x

    def __repr__(self):
        return "F(x={})".format(self.x)


FFAOptions = namedtuple('FFAOptions', ['alpha', 'beta_0', 'gamma'])


class FireflyAlgorithm(base.SwarmIntelligenceAlgorithm):
    def __init__(self, eval_fn, is_solution_better_cmp, update_gui_callback,
                 swarm_size, val_bounds, nb_dim, options):
        super(FireflyAlgorithm, self).__init__(eval_fn, is_solution_better_cmp,
                                               update_gui_callback,
                                               swarm_size, val_bounds, nb_dim,
                                               options)

    def get_random_individual(self):
        min_val, max_val = self.val_bounds
        x = utils.uniform(min_val, max_val, self.nb_dim)
        return Firefly(x)

    def _intensity(self, x):
        return 1.0 / (self.eval_fn(x) + 1e-10)

    def _distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def update_individual(self, ind):
        for ff in self.individuals:
            if self._intensity(ff.x) > self._intensity(ind.x):
                attractiveness = self.options.beta_0 * np.exp(
                    (-1) * self.options.gamma * self._distance(ind.x, ff.x))
                random_factor = utils.uniform(0, 1, self.nb_dim) - 0.5

                ind.x = ind.x + \
                        attractiveness * (ff.x - ind.x) + \
                        self.options.alpha * random_factor
