"""
Particle Swarm Optimization
"""
import numpy as np


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


class PSO(object):
    OMEGA = 0.25
    PHI_P = 2
    PHI_G = 2

    def __init__(self, evaluate_fn, update_gui_callback,
                 nb_particles=50,
                 val_bounds=(-5.12, 5.12),
                 max_iter=500,
                 nb_dim=2):
        self.nb_particles = nb_particles
        self.val_bounds = val_bounds
        self.eval_fn = evaluate_fn
        self.best_x = [9999] * nb_dim
        self.max_iter = max_iter
        self.nb_dim = nb_dim
        self.particles = self._initialize_particles()
        self.update_gui_callback = update_gui_callback

        self.update_gui(-1)

    def _initialize_particles(self):
        min_val = self.val_bounds[0]
        max_val = self.val_bounds[1]

        particles = []

        for i in range(self.nb_particles):
            x = np.random.uniform(min_val, max_val, 2)
            v = np.random.uniform(-1 * abs(max_val - min_val),
                                  abs(max_val - min_val), 2)
            particles.append(Particle(i, x, v))

            if self.eval_fn(*x) < self.eval_fn(*self.best_x):
                self.best_x = x

        return particles

    def run(self):
        for i in range(self.max_iter):
            for p in self.particles:
                for d in range(self.nb_dim):
                    rp = np.random.uniform()
                    rg = np.random.uniform()
                    p.v[d] = PSO.OMEGA * p.v[d] + \
                        PSO.PHI_P * rp * (p.best_x[d] - p.x[d]) + \
                        PSO.PHI_G * rg * (self.best_x[d] - p.x[d])
                p.x = list(np.add(p.x, p.v))

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

        avg_result = sum(all_particle_results)/self.nb_particles

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
