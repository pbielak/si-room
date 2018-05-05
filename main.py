"""
Visualize function and update
"""
import matplotlib.pyplot as plt

from si.algorithm import base
from si.algorithm import bat
from si.algorithm import ffa
from si.algorithm import pso

from si.gui import function
from si.gui import room as room_gui

from si.problem.function_optimization import rastrigin
from si.problem.room_planning import eval as rp_eval
from si.problem.room_planning import room as rp_room


def get_pso(common_options):
    alg = pso.ParticleSwarmOptimization(
        options=pso.PSOOptions(omega=0.25, phi_p=2, phi_g=2),
        **common_options
    )
    return alg


def get_ffa(common_options):
    alg = ffa.FireflyAlgorithm(
        options=ffa.FFAOptions(alpha=0.15, beta_0=0.7, gamma=2),
        **common_options
    )
    return alg


def get_bat(common_options):
    alg = bat.BatAlgorithm(
        options=bat.BatOptions(alpha=0.9, gamma=0.9,
                               f_min=0, f_max=1,
                               A_0=100, A_min=1),
        **common_options
    )
    return alg


def get_rastrigin_problem():
    eval_fn = lambda x: rastrigin.rastrigin_fn(*x)

    gui = function.FunctionGUI(eval_fn=eval_fn,
                               val_bounds=(-5.12, 5.12),
                               restricted=2)

    common_options = dict(eval_fn=eval_fn,
                          update_gui_callback=gui.update_points,
                          is_solution_better_cmp=base.minimization_problem_cmp(),
                          nb_dim=2, val_bounds=(-5.12, 5.12),
                          swarm_size=30)

    return gui, eval_fn, common_options


def get_room_problem():
    eval_fn = lambda x: rp_eval.evaluate_room(
        rp_room.solution_to_room(x, rp_room.Room(40, 40)))

    gui = room_gui.RoomGUI(room=rp_room.Room(40, 40),
                           eval_fn=eval_fn)

    common_options = dict(eval_fn=eval_fn,
                          update_gui_callback=gui.update_points,
                          is_solution_better_cmp=base.maximization_problem_cmp(),
                          nb_dim=20, val_bounds=(-20, 20),
                          swarm_size=30)

    return gui, eval_fn, common_options


def run_algorithm(problem_fn, alg_fn, nb_iterations):
    gui, eval_fn, common_options = problem_fn()
    gui.draw()

    alg = alg_fn(common_options)

    alg.run(max_iter=nb_iterations)

    fmt_str = 'Best solution {} => {}'
    print(fmt_str.format(alg.best_x, eval_fn(alg.best_x)))


def main():
    # run_algorithm(get_rastrigin_problem, get_pso, 175)
    run_algorithm(get_room_problem, get_pso, 175)


if __name__ == '__main__':
    main()
    plt.show(block=True)
