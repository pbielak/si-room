"""
Base classes for algorithm
"""


class SwarmIntelligenceAlgorithm(object):
    def __init__(self, eval_fn, update_gui_callback):
        self.eval_fn = eval_fn
        self.update_gui_callback = update_gui_callback

    def run(self, max_iter):
        pass

    def update_gui(self, iteration):
        pass
