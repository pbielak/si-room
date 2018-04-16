"""
Visualize function and update
"""
import matplotlib.pyplot as plt

from si.algorithm import pso
from si.gui import rastrigin


def main():
    rfg = rastrigin.RastriginFunctionGUI()
    rfg.draw()
    alg = pso.ParticleSwarmOptimization(eval_fn=rastrigin.rastrigin_fn,
                                        update_gui_callback=rfg.update_points,
                                        nb_particles=10)
    alg.run(max_iter=175)

    print('Best particle:',
          alg.best_x,
          '=>',
          rastrigin.rastrigin_fn(*alg.best_x))


if __name__ == '__main__':
    main()
    plt.show(block=True)