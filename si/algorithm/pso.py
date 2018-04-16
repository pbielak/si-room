"""
Particle Swarm Optimization
"""
import numpy as np

from si.algorithm import base


def uniform(min_val=0, max_val=1, size=2):
    return np.random.uniform(min_val, max_val, size)


class Particle(object):
    def __init__(self, pid, x, v):
        self.pid = pid
        self.x = x
        self.v = v
        self.best_x = x

    def __repr__(self):
        return "P(ID={}, pos={}, vel={})".format(
            self.pid, self.x, self.v
        )


class ParticleSwarmOptimization(base.SwarmIntelligenceAlgorithm):
    OMEGA = 0.25
    PHI_P = 2
    PHI_G = 2

    def __init__(self, eval_fn, update_gui_callback,
                 nb_particles=50,
                 val_bounds=(-5.12, 5.12),
                 nb_dim=2):
        super(ParticleSwarmOptimization, self).__init__(eval_fn,
                                                        update_gui_callback)

        self.val_bounds = val_bounds
        self.best_x = [9999] * nb_dim
        self.nb_dim = nb_dim

        self.particles = self._generate_particles(nb_particles)
        self.update_gui(-1)

    def _generate_particles(self, nb_particles):
        min_val = self.val_bounds[0]
        max_val = self.val_bounds[1]

        particles = []

        for i in range(nb_particles):
            x = uniform(min_val, max_val, 2)
            v = uniform(-1 * abs(max_val - min_val),
                        abs(max_val - min_val), 2)
            particles.append(Particle(i, x, v))

            if self.eval_fn(*x) < self.eval_fn(*self.best_x):
                self.best_x = x

        return particles

    def run(self, max_iter):
        for i in range(max_iter):
            for p in self.particles:
                rp = uniform(size=self.nb_dim)
                rg = uniform(size=self.nb_dim)
                p.v = self.OMEGA * p.v + \
                      self.PHI_P * rp * (p.best_x - p.x) + \
                      self.PHI_G * rg * (self.best_x - p.x)

                p.x = p.x + p.v

                if self.eval_fn(*p.x) < self.eval_fn(*p.best_x):
                    p.best_x = p.x
                    if self.eval_fn(*p.best_x) < self.eval_fn(*self.best_x):
                        self.best_x = p.best_x

            self.update_gui(i)

    def update_gui(self, iteration):
        if not self.update_gui_callback:
            return

        if self.nb_dim != 2:
            raise ValueError("Can visualize only 3D plots (NB_DIM must be 2)!")

        all_particle_results = list(map(lambda p: self.eval_fn(*p.x),
                                        self.particles))

        avg_result = sum(all_particle_results)/len(self.particles)

        msg = 'Iteration: {} \n' \
              '(current best: {} => {})\n' \
              'Avg result: {}'.format(
            iteration, np.round(self.best_x, 2),
            np.round(self.eval_fn(*self.best_x), 2),
            np.round(avg_result, 2)
        )
        pts_x = list(map(lambda p: p.x[0], self.particles))
        pts_y = list(map(lambda p: p.x[1], self.particles))
        self.update_gui_callback(msg, (pts_x, pts_y), (iteration, avg_result))
