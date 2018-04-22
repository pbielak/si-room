"""
Particle Swarm Optimization
"""
from si.algorithm import base


class Particle(base.Individual):
    def __init__(self, x, v):
        super(Particle, self).__init__(x)
        self.v = v
        self.best_x = x

    def get_best(self):
        return self.best_x

    def __repr__(self):
        return "P(pos={}, vel={})".format(self.x, self.v)


class PSOOptions(base.SIAlgorithmOptions):
    def __init__(self, omega, phi_p, phi_g, eval_fn,
                 update_gui_callback, swarm_size,
                 val_bounds, nb_dim):
        super(PSOOptions, self).__init__(eval_fn, update_gui_callback,
                                         swarm_size, val_bounds, nb_dim)
        self.omega = omega
        self.phi_p = phi_p
        self.phi_g = phi_g


class ParticleSwarmOptimization(base.SwarmIntelligenceAlgorithm):
    def __init__(self, cfg: PSOOptions):
        super(ParticleSwarmOptimization, self).__init__(cfg)

    def get_random_individual(self):
        min_val, max_val = self.cfg.val_bounds

        x = base.uniform(min_val, max_val, self.cfg.nb_dim)
        v = base.uniform(-1 * abs(max_val - min_val),
                         abs(max_val - min_val), self.cfg.nb_dim)
        return Particle(x, v)

    def update_individual(self, ind):
        rp = base.uniform(size=self.cfg.nb_dim)
        rg = base.uniform(size=self.cfg.nb_dim)
        ind.v = self.cfg.omega * ind.v + \
              self.cfg.phi_p * rp * (ind.best_x - ind.x) + \
              self.cfg.phi_g * rg * (self.best_x - ind.x)

        ind.x = ind.x + ind.v

        if self.cfg.eval_fn(*ind.x) < self.cfg.eval_fn(*ind.best_x):
            ind.best_x = ind.x
