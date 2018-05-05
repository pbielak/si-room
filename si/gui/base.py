"""
Base classes for GUI
"""
import matplotlib.pyplot as plt
import numpy as np


class GUI(object):
    def __init__(self, eval_fn, draw_bounds):
        self.eval_fn = eval_fn
        self.draw_bounds = draw_bounds
        self.fig = None
        self._setup()

    def _setup(self):
        plt.ion()
        self.fig = plt.figure(figsize=(14, 7))

    def draw(self):
        self._draw()
        plt.show()

    def _draw(self):
        pass

    def update_points(self, iteration, swarm, best_x):
        pass


class GUIWithSummaryPlot(GUI):
    def __init__(self, eval_fn, draw_bounds):
        self.summary_ax = None
        self.summary_x = []
        self.avg_results_y = []
        self.best_result_y = []

        super(GUIWithSummaryPlot, self).__init__(eval_fn, draw_bounds)

    def _setup(self):
        super(GUIWithSummaryPlot, self)._setup()

        self.summary_ax = self.fig.add_subplot(122)

        self.summary_ax.set_title('Summary')
        self.summary_ax.plot(0, 0,
                             color='g',
                             label='Avg')
        self.summary_ax.plot(0, 0,
                             color='r',
                             linestyle='--',
                             label='Best')
        self.summary_ax.set_xlabel('Iteration')
        self.summary_ax.set_ylabel('Fitness')
        self.summary_ax.legend()

    def update_points(self, iteration, swarm, best_x):
        msg = 'Iteration: {} \n(current best: {} => {})\n'.format(
            iteration, np.round(best_x, 2),
            np.round(self.eval_fn(best_x), 2)
        )
        self.fig.suptitle(msg)

        avg_result = sum(map(lambda p: self.eval_fn(p.x), swarm)) / len(swarm)
        best_result = self.eval_fn(best_x)

        self.summary_x.append(iteration)

        self.avg_results_y.append(avg_result)
        self.best_result_y.append(best_result)

        self.summary_ax.plot(self.summary_x,
                             self.avg_results_y,
                             color='g',
                             label='Avg')
        self.summary_ax.plot(self.summary_x,
                             self.best_result_y,
                             color='r',
                             linestyle='--',
                             label='Best')
