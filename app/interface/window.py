from tkinter import *
from typing import Optional

from matplotlib.figure import Figure

from app.experiment import Experiment
from app.interface.style import Style
from graph import FigureTk, MotionGraphHandler, PlayControls
from mechanics import Universe
from .controls import SimulationControls
from .pane import ListPane, ExperimentPane, UniversePane, SimulationPane


class ExperimentWindow(Tk):
    experiment: Experiment
    universe: Universe

    figureframe: FigureTk
    controls: PlayControls = None
    simulation: MotionGraphHandler = None
    figure: Figure
    experiment_pane: ListPane
    simulation_pane: ListPane
    universe_pane: ListPane


    def __init__(self, experiment: Experiment, universe: Universe, simulation: MotionGraphHandler = None, style: Style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.experiment = experiment
        self.universe: universe
        self.style = style or Style()

        self.config(**self.style.frame_format)
        self.title(experiment.name)
        self.resizable(True, False)

        self.figureframe = FigureTk(self)
        self.figure = self.figureframe.canvas.figure
        self.figure.patch.set_facecolor(self.style.graph_background)

        self.leftpane = Frame(self, **self.style.frame_format)
        self.experiment_pane = ExperimentPane(self.leftpane, self, experiment,
                                              buttonconf=self.style.special_button_format,
                                              labelconf=self.style.label_format,
                                              entryconf=self.style.entry_format,
                                              **self.style.frame_format
                                              )
        self.universe_pane = UniversePane(self.leftpane, experiment, universe,
                                          specialbuttonconf=self.style.special_button_format,
                                          buttonconf=self.style.button_format,
                                          labelconf=self.style.label_format,
                                          entryconf=self.style.entry_format,
                                          **self.style.frame_format
                                          )
        self.simulation_pane = SimulationPane(self, experiment, universe,
                                              buttonconf=self.style.button_format,
                                              labelconf=self.style.label_format,
                                              entryconf=self.style.entry_format,
                                              specialbuttonconf=self.style.special_button_format,
                                              **self.style.frame_format
                                              )

        self.leftpane.grid(row=0, column=0, sticky=N+S+E+W)
        self.experiment_pane.pack(fill=X)
        self.universe_pane.pack(fill=X)
        self.simulation_pane.grid(row=0, column=2, rowspan=2, sticky=N+E+W)
        self.figureframe.grid(row=0, column=1)

        if simulation:
            self.add_simulation(simulation)

    def title(self, title: str="") -> Optional[str]:
        if not title:
            return super().title()
        super().title(f"gravity - {title}")

    def add_simulation(self, simulation: MotionGraphHandler):
        self.simulation_pane.simulation = simulation
        self.controls = SimulationControls(self, simulation.animations, styling=self.style.button_format)
        self.controls.grid(column=1, row=2)
        self.simulation = simulation
        self.simulation.axes.set_facecolor(self.style.graph_background)
