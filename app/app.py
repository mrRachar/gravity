import math as maths
from tkinter import mainloop
from typing import List

from .interface.window import ExperimentWindow

from app.experiment import Experiment
from app.interface.style import Style
from graph import MotionGraphHandler, Animation
from mechanics import Gravity, Universe, Particle, Coords, Velocity


class SimulationAnimation(Animation):
    playing = False
    experiment: Experiment

    def __init__(self, experiment: Experiment):
        super().__init__()
        self.experiment = experiment

    def step(self, n: int, graph, universe):
        for x in range(int(self.experiment.speed)):
            universe.tick(n)
        graph.update_positions()

class App:
    experiment_windows: List[ExperimentWindow]
    welcome_window = None
    style = None

    def __init__(self):
        self.style = Style()

    def demo(self):
        experiment = Experiment("Lunar Orbit", Universe([Gravity(6.67408e-11)]))

        experiment.universe <<= Particle(7.342e22, Coords(384.4e6, 0, (384.4e6 * maths.tan(maths.radians(5.14)))), Velocity(1022, 0), colour="grey")
        experiment.universe <<= Particle(5.97237e24, Coords(0, 0, 0), Velocity(0, 0), colour="blue")
        self.load_experiment(experiment)

    def load_experiment(self, experiment: Experiment):
        universe = experiment.universe.copy()
        window = ExperimentWindow(experiment, universe, style=self.style)
        window.iconbitmap(default='./app/rsc/icon.ico')
        axes = window.figure.add_subplot(111, projection='3d')
        graph = MotionGraphHandler(universe, figure=window.figure, axes=axes)
        window.add_simulation(graph)
        graph.ensure_lines()

        graph.figure.suptitle(experiment.name)
        graph.add_animation(SimulationAnimation(experiment))

        graph.fit_all()

        mainloop()

