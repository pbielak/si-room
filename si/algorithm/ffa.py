"""
Firefly algorithm
"""
import numpy as np

from si.algorithm import base


class Firefly(base.Individual):
    def __init__(self, x):
        super(Firefly, self).__init__(x)

    def get_best(self):
        return self.x

    def __repr__(self):
        return "F(x={})".format(self.x)


class FFAOptions(base.SIAlgorithmOptions):
    def __init__(self, alpha, beta_0, gamma, eval_fn,
                 update_gui_callback, swarm_size,
                 val_bounds, nb_dim):
        super(FFAOptions, self).__init__(eval_fn, update_gui_callback,
                                         swarm_size, val_bounds, nb_dim)
        self.alpha = alpha
        self.beta_0 = beta_0
        self.gamma = gamma


class FireflyAlgorithm(base.SwarmIntelligenceAlgorithm):
    def __init__(self, cfg: FFAOptions):
        super(FireflyAlgorithm, self).__init__(cfg)

    def get_random_individual(self):
        min_val, max_val = self.cfg.val_bounds
        x = base.uniform(min_val, max_val, self.cfg.nb_dim)
        return Firefly(x)

    def _intensity(self, x):
        return 1.0 / (self.cfg.eval_fn(*x) + 1e-10)

    def _distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def update_individual(self, ind):
        for ff in self.individuals:
            if self._intensity(ff.x) > self._intensity(ind.x):
                attractiveness = self.cfg.beta_0 * np.exp(
                    (-1) * self.cfg.gamma * self._distance(ind.x, ff.x))
                random_factor = base.uniform(0, 1, self.cfg.nb_dim) - 0.5

                ind.x = ind.x + \
                        attractiveness * (ff.x - ind.x) + \
                        self.cfg.alpha * random_factor
