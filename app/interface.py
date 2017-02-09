from tkinter import *
from typing import List

from matplotlib.figure import Figure

from graph import *

class SimulationControls(PlayControls):
    animations: List[Animation]
    def __init__(self, master, animations: List[Animation], *args, **kwargs):
        super().__init__(self, master, *args, **kwargs)
        self.animations = animations

    def play(self):
        for animation in self.animations:
            animation.play()

    def pause(self):
        for animation in self.animations:
            animation.pause()


class GravityWindow(Tk):
    figureframe: FigureTk
    controls: PlayControls = None
    simulation: MotionGraphHandler = None
    figure: Figure

    def __init__(self, simulation: MotionGraphHandler=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gravity Simulation")
        self.figureframe = FigureTk(self)
        self.figureframe.grid(row=0, column=0)
        self.figure = self.figureframe.canvas.figure
        if simulation:
            self.add_simulation(simulation)

    def add_simulation(self, simulation: MotionGraphHandler):
        self.controls = SimulationControls(self, simulation.animations)
        self.controls.grid(column=0, row=1)
        self.simulation = simulation