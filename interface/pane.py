from tkinter import Frame, Label, Widget

from graph import MotionGraphHandler
from app.experiment import Experiment
from .input import UserEntry, Vector3DEntry

class PropertiesPane(list, Frame):
    title: str
    titlelabel: Label

    def __init__(self, master, title: str, **kwargs):
        Frame.__init__(self, master, **kwargs)
        list.__init__(self)

        self.title = title
        self.titlelabel = Label(self, text=title)
        self.titlelabel.pack()

    def append(self, widget: Widget):
        widget.pack()
        super().append(widget)

    def __delitem__(self, index):
        self[index].pack_forget()
        super().__delitem__(index)


class SimulationPane(PropertiesPane):
    __simulation = None

    def __init__(self, master, simulation: MotionGraphHandler=None):
        super().__init__(master, 'Simulation')
        self.simulation = simulation

    @property
    def simulation(self) -> MotionGraphHandler:
        return self.__simulation

    @simulation.setter
    def simulation(self, sim: MotionGraphHandler):
        self.__simulation = sim


class ExperimentPane(PropertiesPane):
    experiment: Experiment

    def __init__(self, master, experiment: Experiment):
        super().__init__(master, 'Experiment')
        self.experiment = experiment

        self.speedentry = Vector3DEntry(self, label="Playback Speed")
        self.nameentry = TextEntry(self, label="Name")