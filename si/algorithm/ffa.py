"""
Firefly algorithm
"""
import numpy as np

from si.algorithm import base


def uniform(min_val=0, max_val=1, size=2):
    return np.random.uniform(min_val, max_val, size)


class Firefly(object):
    def __init__(self, fid, x):
        self.fid = fid
        self.x = x

    def __repr__(self):
        return "F(ID={}, x={})".format(self.fid, self.x)


class FireflyAlgorithm(base.SwarmIntelligenceAlgorithm):
    ALPHA = 0.15
    BETA_0 = 0.7
    GAMMA = 2

    def __init__(self, eval_fn, update_gui_callback,
                 nb_fireflies=50,
                 val_bounds=(-5.12, 5.12),
                 nb_dim=2):
        super(FireflyAlgorithm, self).__init__(eval_fn, update_gui_callback)

        self.val_bounds = val_bounds
        self.best_x = [9999] * nb_dim
        self.nb_dim = nb_dim

        self.fireflies = self._generate_fireflies(nb_fireflies)
        self.update_gui(-1)

    def _generate_fireflies(self, nb_fireflies):
        min_val = self.val_bounds[0]
        max_val = self.val_bounds[1]

        fireflies = []

        for i in range(nb_fireflies):
            x = uniform(min_val, max_val, self.nb_dim)
            fireflies.append(Firefly(i, x))

        return fireflies

    def _intensity(self, x):
        return 1.0 / self.eval_fn(*x)

    def _distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def run(self, max_iter):
        for i in range(max_iter):
            for f in self.fireflies:
                for ff in self.fireflies:
                    if self._intensity(ff.x) > self._intensity(f.x):
                        attractiveness = self.BETA_0 * np.exp((-1) * self.GAMMA * self._distance(f.x, ff.x))
                        random_factor = uniform(0, 1, self.nb_dim) - 0.5

                        f.x = f.x + \
                              attractiveness * (ff.x - f.x) + \
                              self.ALPHA * random_factor

            for f in self.fireflies:
                if self.eval_fn(*f.x) < self.eval_fn(*self.best_x):
                    self.best_x = f.x

            self.update_gui(i)

    def update_gui(self, iteration):
        if not self.update_gui_callback:
            return

        if self.nb_dim != 2:
            raise ValueError("Can visualize only 3D plots (NB_DIM must be 2)!")

        all_fireflies_results = list(map(lambda p: self.eval_fn(*p.x),
                                         self.fireflies))

        avg_result = sum(all_fireflies_results)/len(self.fireflies)

        msg = 'Iteration: {} \n' \
              '(current best: {} => {})\n' \
              'Avg result: {}'.format(
            iteration, np.round(self.best_x, 2),
            np.round(self.eval_fn(*self.best_x), 2),
            np.round(avg_result, 2)
        )
        pts_x = list(map(lambda p: p.x[0], self.fireflies))
        pts_y = list(map(lambda p: p.x[1], self.fireflies))
        self.update_gui_callback(msg, (pts_x, pts_y), (iteration, avg_result))
