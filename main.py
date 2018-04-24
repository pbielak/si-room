"""
Visualize function and update
"""
import matplotlib.pyplot as plt

from si.algorithm import pso
from si.algorithm import ffa
from si.gui import function
from si.problem.function_optimization import rastrigin


def common_options(eval_fn, gui_callback):
    return dict(eval_fn=eval_fn,
                update_gui_callback=gui_callback,
                swarm_size=20, val_bounds=(-2, 2),#val_bounds=(-5.12, 5.12),
                nb_dim=2)


def get_pso(eval_fn, gui_callback):
    alg = pso.ParticleSwarmOptimization(
        options=pso.PSOOptions(omega=0.25, phi_p=2, phi_g=2),
        **common_options(eval_fn, gui_callback)
    )
    return alg


def get_ffa(eval_fn, gui_callback):
    alg = ffa.FireflyAlgorithm(
        options=ffa.FFAOptions(alpha=0.15, beta_0=0.7, gamma=2),
        **common_options(eval_fn, gui_callback)
    )
    return alg


def main():
    rfg = function.FunctionGUI(func=rastrigin.rastrigin_fn,
                               val_range=(-5.12, 5.12),
                               restricted=2)
    rfg.draw()

    # alg = get_pso(rastrigin.rastrigin_fn, rfg.update_points)
    alg = get_ffa(rastrigin.rastrigin_fn, rfg.update_points)

    alg.run(max_iter=175)

    print('Best solution:',
          alg.best_x,
          '=>',
          rastrigin.rastrigin_fn(*alg.best_x))


if __name__ == '__main__':
    main()
    plt.show(block=True)
