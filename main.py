"""
Visualize function and update
"""
import matplotlib.pyplot as plt

from si import pso
from si.gui import rastrigin


def main():
    rfg = rastrigin.RastriginFunctionGUI()
    rfg.draw()
    alg = pso.PSO(evaluate_fn=rastrigin.rastrigin_fn,
                  update_gui_callback=rfg.update_points,
                  nb_particles=20)
    alg.run()


if __name__ == '__main__':
    main()
    plt.show(block=True)