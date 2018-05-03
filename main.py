"""
Visualize function and update
"""
import matplotlib.pyplot as plt

from si.algorithm import bat
from si.algorithm import ffa
from si.algorithm import pso
from si.gui import function
from si.gui.room import RoomGUI
from si.problem.function_optimization import rastrigin
from si.problem.room_planning.eval import evaluate_room
from si.problem.room_planning.room import Room, load_default_room_furniture, \
    solution_to_room


def common_options(eval_fn, gui_callback):
    return dict(eval_fn=eval_fn,
                update_gui_callback=gui_callback,
                swarm_size=20, val_bounds=(-20, 20),#val_bounds=(-5.12, 5.12),
                nb_dim=20)


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


def get_bat(eval_fn, gui_callback):
    alg = bat.BatAlgorithm(
        options=bat.BatOptions(alpha=0.9, gamma=0.9,
                               f_min=0, f_max=1,
                               A_0=100, A_min=1),
        **common_options(eval_fn, gui_callback)
    )
    return alg


def main():
    # gui = function.FunctionGUI(func=rastrigin.rastrigin_fn,
    #                            val_range=(-5.12, 5.12),
    #                            restricted=2)
    room = Room(40, 40)
    gui = RoomGUI(room)
    gui.draw()

    # eval_fn = lambda x: rastrigin.rastrigin_fn(*x)
    eval_fn = lambda x: 1.0 / evaluate_room(solution_to_room(x, room))

    # alg = get_bat(eval_fn, gui.update_points)
    # alg = get_ffa(eval_fn, gui.update_points)
    alg = get_pso(eval_fn, gui.update_points)

    alg.run(max_iter=175)

    print('Best solution:',
          alg.best_x,
          '=>',
          eval_fn(alg.best_x))


if __name__ == '__main__':
    main()
    plt.show(block=True)
