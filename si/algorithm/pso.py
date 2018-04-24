"""
Particle Swarm Optimization
"""
from collections import namedtuple

from si.algorithm import base
from si import utils


class Particle(base.Individual):
    def __init__(self, x, v):
        super(Particle, self).__init__(x)
        self.v = v
        self.best_x = x

    def get_best(self):
        return self.best_x

    def __repr__(self):
        return "P(pos={}, vel={})".format(self.x, self.v)


PSOOptions = namedtuple('PSOOptions', ['omega', 'phi_p', 'phi_g'])


class ParticleSwarmOptimization(base.SwarmIntelligenceAlgorithm):
    def __init__(self, eval_fn, update_gui_callback,
                 swarm_size, val_bounds, nb_dim, options):
        super(ParticleSwarmOptimization, self).__init__(eval_fn,
                                                        update_gui_callback,
                                                        swarm_size, val_bounds,
                                                        nb_dim, options)

    def get_random_individual(self):
        min_val, max_val = self.val_bounds

        x = utils.uniform(min_val, max_val, self.nb_dim)
        v = utils.uniform(-1 * abs(max_val - min_val),
                          abs(max_val - min_val), self.nb_dim)
        return Particle(x, v)

    def update_individual(self, ind):
        rp = utils.uniform(size=self.nb_dim)
        rg = utils.uniform(size=self.nb_dim)
        ind.v = self.options.omega * ind.v + \
                self.options.phi_p * rp * (ind.best_x - ind.x) + \
                self.options.phi_g * rg * (self.best_x - ind.x)

        ind.x = ind.x + ind.v

        if self.eval_fn(*ind.x) < self.eval_fn(*ind.best_x):
            ind.best_x = ind.x
