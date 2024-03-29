"""
Base classes for algorithm
"""
import numpy as np


def minimization_problem_cmp():
    return lambda x, y: x < y


def maximization_problem_cmp():
    return lambda x, y: x > y


class Individual(object):
    def __init__(self, x):
        self.x = x

    def get_best(self):
        pass


class SwarmIntelligenceAlgorithm(object):
    def __init__(self, eval_fn, is_solution_better_cmp, update_gui_callback,
                 swarm_size, val_bounds, nb_dim, options):
        self.eval_fn = eval_fn
        self.is_solution_better_cmp = is_solution_better_cmp
        self.update_gui_callback = update_gui_callback
        self.swarm_size = swarm_size
        self.val_bounds = val_bounds
        self.nb_dim = nb_dim
        self.options = options

        self.best_x = [9999] * self.nb_dim
        self.individuals = self.generate_individuals()
        self.update_gui(-1)

    def generate_individuals(self):
        individuals = []

        for i in range(self.swarm_size):
            ind = self.get_random_individual()
            individuals.append(ind)

            if self.is_solution_better_cmp(self.eval_fn(ind.x),
                                           self.eval_fn(self.best_x)):
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
                                self.val_bounds[0],
                                self.val_bounds[1])

                if self.is_solution_better_cmp(self.eval_fn(ind.get_best()),
                                               self.eval_fn(self.best_x)):
                    self.best_x = ind.get_best()

            self.update_gui(i)

    def update_gui(self, iteration):
        if not self.update_gui_callback:
            return

        self.update_gui_callback(iteration, self.individuals, self.best_x)
