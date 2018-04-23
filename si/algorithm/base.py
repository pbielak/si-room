"""
Base classes for algorithm
"""
import numpy as np


class Individual(object):
    def __init__(self, x):
        self.x = x

    def get_best(self):
        pass


class SIAlgorithmOptions(object):
    def __init__(self, eval_fn, update_gui_callback,
                 swarm_size, val_bounds, nb_dim):
        self.eval_fn = eval_fn
        self.update_gui_callback = update_gui_callback
        self.swarm_size = swarm_size
        self.val_bounds = val_bounds
        self.nb_dim = nb_dim


class SwarmIntelligenceAlgorithm(object):
    def __init__(self, cfg: SIAlgorithmOptions):
        self.cfg = cfg
        self.best_x = [9999] * self.cfg.nb_dim
        self.individuals = self.generate_individuals()
        self.update_gui(-1)

    def generate_individuals(self):
        individuals = []

        for i in range(self.cfg.swarm_size):
            ind = self.get_random_individual()
            individuals.append(ind)

            if self.cfg.eval_fn(*ind.x) < self.cfg.eval_fn(*self.best_x):
                self.best_x = ind.x

        return individuals

    def get_random_individual(self):
        pass

    def update_individual(self, ind):
        pass

    def run(self, max_iter):
        for i in range(max_iter):
            for ind in self.individuals:
                self.update_individual(ind)
                ind.x = np.clip(ind.x,
                                self.cfg.val_bounds[0],
                                self.cfg.val_bounds[1])

                if self.cfg.eval_fn(*ind.get_best()) < self.cfg.eval_fn(*self.best_x):
                    self.best_x = ind.get_best()

            self.update_gui(i)

    def update_gui(self, iteration):
        if not self.cfg.update_gui_callback:
            return

        if self.cfg.nb_dim != 2:
            raise ValueError("Can visualize only 3D plots (NB_DIM must be 2)!")

        all_particle_results = list(map(lambda p: self.cfg.eval_fn(*p.x),
                                        self.individuals))

        avg_result = sum(all_particle_results)/len(self.individuals)

        msg = 'Iteration: {} \n' \
              '(current best: {} => {})\n' \
              'Avg result: {}'.format(
            iteration, np.round(self.best_x, 2),
            np.round(self.cfg.eval_fn(*self.best_x), 2),
            np.round(avg_result, 2)
        )
        pts_x = list(map(lambda p: p.x[0], self.individuals))
        pts_y = list(map(lambda p: p.x[1], self.individuals))
        self.cfg.update_gui_callback(msg, (pts_x, pts_y),
                                     (iteration, avg_result))


def uniform(min_val=0, max_val=1, size=2):
    return np.random.uniform(min_val, max_val, size)
