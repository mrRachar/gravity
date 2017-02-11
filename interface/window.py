from tkinter import Tk

from matplotlib.figure import Figure

from graph import FigureTk
from graph import MotionGraphHandler
from graph import PlayControls
from .controls import SimulationControls
from .pane import PropertiesPane, ExperimentPane, SimulationPane


class GravityWindow(Tk):
    figureframe: FigureTk
    controls: PlayControls = None
    simulation: MotionGraphHandler = None
    figure: Figure
    experiment_pane: PropertiesPane
    simulation_pane: PropertiesPane

    window_styling = {
        'bg': "#4f4f4f",
    }
    widget_styling = {
        'bg': "#444444",
        'fg': "#eeeeee",
        'relief': "groove",
    }
    graph_styling = {
        'bg': '#efefef'
    }

    def __init__(self, experiment, simulation: MotionGraphHandler = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.experiment = experiment

        self.config(**self.window_styling)
        self.title("Gravity Simulation")

        self.figureframe = FigureTk(self)
        self.figure = self.figureframe.canvas.figure
        self.figure.patch.set_facecolor(self.graph_styling['bg'])

        self.experiment_pane = ExperimentPane(self, experiment)
        self.simulation_pane = SimulationPane(self)

        self.experiment_pane.grid(row=0, column=0, rowspan=2)
        self.simulation_pane.grid(row=0, column=2, rowspan=2)
        self.figureframe.grid(row=0, column=1)

        if simulation:
            self.add_simulation(simulation)

    def add_simulation(self, simulation: MotionGraphHandler):
        self.simulation_pane.simulation = simulation
        self.controls = SimulationControls(self, simulation.animations, styling=self.widget_styling)
        self.controls.grid(column=0, row=1)
        self.simulation = simulation
        self.simulation.axes.set_facecolor(self.graph_styling['bg'])
