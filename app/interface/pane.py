from tkinter import *
from tkinter.colorchooser import askcolor
from typing import List, Dict, Any, Union

from graph import Line3DHandler, MotionGraphHandler
from app.experiment import Experiment
from mechanics import Gravity, Universe, Particle, Velocity, Coords
from .input import UserEntry, Vector3DEntry, ResetableUserEntry, ResetableVector3DEntry


class StackReplacementException(Exception): pass

class ListPane(Frame):
    titlename: str
    titlelabel: Label
    widgets: List[Widget]
    start_from: str

    def __init__(self, master, title: str, labelconf: Dict[str, Any]=None, start_from=TOP, packconfig=None, **kwargs):
        config = {
            'padx': 5,
            'pady': 5,
        }
        config.update(kwargs)
        super().__init__(master=master, **config)

        _labelconf = {
            'padx': 5,
            'pady': 5,
            'font': ('Veranda', 10, 'bold')
        }
        _labelconf.update(labelconf or {})

        self.start_from=start_from
        self.widgets = []
        self.titlename = title
        self.titlelabel = Label(self, text=title, **_labelconf)
        self.titlelabel.pack(anchor=W)
        self.packconfig = packconfig or {}

    def append(self, widget: Widget):
        widget.pack(fill=X, expand=1, anchor=E, side=self.start_from, **self.packconfig)
        self.widgets.append(widget)

    def __delitem__(self, index):
        self[index].pack_forget()
        del self.widgets[index]

    def __getitem__(self, index: int):
        return self.widgets[index]

    def __setitem__(self, index: int, widget: Widget):
        raise StackReplacementException("ListPane items cannot be replaced")

    def __iter__(self):
        return iter(self.widgets)

    def clear(self):
        for index, _ in reversed(list(enumerate(self))):
            del self[index]

class SimpleListPane(ListPane):
    def __init__(self, master, start_from: str=TOP, **kwargs):
        super().__init__(master, '', start_from=start_from, **kwargs)
        self.titlelabel.pack_forget()


class SimulationPane(ListPane):
    simulation: MotionGraphHandler
    universe: Universe
    experiment: Experiment

    def __init__(self, master, experiment: Experiment, universe: Universe, simulation: MotionGraphHandler=None,
                 entryconf: Dict[str, Any]=None,
                 labelconf: Dict[str, Any]=None,
                 specialbuttonconf: Dict[str, Any]=None,
                 buttonconf: Dict[str, Any]=None,
                 **kwargs
                 ):
        super().__init__(master, 'Simulation', labelconf=labelconf, **kwargs)
        self.simulation = simulation
        self.experiment = experiment
        self.universe = universe
        self.entryconf = entryconf or {}
        self.specialbuttonconf = specialbuttonconf or {}
        self.buttonconf = buttonconf or {}
        self.labelconf = labelconf or {}
        self.frameconf = kwargs

    def load_particles(self):
        self.clear()
        for experiment_particle, universe_particle in zip(self.experiment.universe.particles, self.universe.particles):
            self.append(ParticleWidget(self, self.experiment.universe, self.universe, self.simulation,
                                       experiment_particle, universe_particle,
                                       self.simulation.particle_lines[universe_particle],
                                       entryconf=self.entryconf,
                                       specialbuttonconf=self.specialbuttonconf,
                                       buttonconf=self.buttonconf,
                                       labelconf=self.labelconf,
                                       **self.frameconf
                                       ))


class ExperimentPane(ListPane):
    experiment: Experiment

    def __init__(self, master, window,
                 experiment: Experiment,
                 labelconf: Dict[str, Any]=None,
                 entryconf: Dict[str, Any]=None,
                 buttonconf: Dict[str, Any]=None,
                 **conf
                 ):
        super().__init__(master, 'Experiment', labelconf=labelconf, **conf)
        self.window = window
        self.experiment = experiment

        self.speedentry = UserEntry(self, placeholder="200", label="Playback Speed", labelconf=labelconf, entryconf=entryconf, **conf)
        self.nameentry = UserEntry(self, placeholder="My Experiment", label="Name", labelconf=labelconf, entryconf=entryconf, **conf)
        self.button = Button(self, text="Apply", command=self.apply_values, **(buttonconf or {}))

        self.speedentry.entry['justify'] = RIGHT

        self.update_values()

        self.append(self.nameentry)
        self.append(self.speedentry)
        self.append(self.button)

        self.button.pack_configure(anchor=E, fill=NONE, padx=3, pady=6)

    def update_values(self):
        self.speedentry.value = str(self.experiment.speed)
        self.nameentry.value = self.experiment.name

    def apply_values(self):
        self.experiment.speed = int(float(self.speedentry.value))
        self.experiment.name = self.nameentry.value.strip('\n \t')
        self.window.simulation.figure.suptitle(self.experiment.name)
        self.window.title(self.experiment.name)
        self.update_values()


class UniversePane(ListPane):
    experiment: Experiment

    def __init__(self, master,
                 experiment: Experiment,
                 universe: Universe,
                 labelconf: Dict[str, Any]=None,
                 entryconf: Dict[str, Any]=None,
                 buttonconf: Dict[str, Any]=None,
                 specialbuttonconf: Dict[str, Any]=None,
                 **conf
                 ):
        super().__init__(master, 'Universe', labelconf=labelconf, **conf)
        self.universe = universe
        self.experiment = experiment
        self.experiment_gfield = experiment.universe.fields[0]
        self.gfield: Gravity = universe.fields[0]

        self.gconstentry = ResetableUserEntry(self,
                                              label="G-constant",
                                              labelconf=labelconf,
                                              entryconf=entryconf,
                                              buttonconf=buttonconf,
                                              resetfunc=lambda entry, content: str(self.experiment_gfield.G),
                                              **conf
                                              )
        self.buttons = Frame(self, **conf)
        self.testbutton = Button(self.buttons, text="Test", command=self.test_values, **(buttonconf or {}))
        self.applybutton = Button(self.buttons, text="Apply", command=self.apply_values, **(specialbuttonconf or {}))

        self.update_values()

        self.append(self.gconstentry)
        self.append(self.buttons)
        self.buttons.pack_configure(fill=X)
        self.applybutton.pack(side=RIGHT, padx=3, pady=6)
        self.testbutton.pack(side=RIGHT, padx=3, pady=6)

    def update_values(self):
        self.gconstentry.value = str(self.gfield.G)

    def apply_values(self):
        self.gfield.G = self.experiment_gfield.G = float(self.gconstentry.value)

    def test_values(self):
        self.gfield.G = float(self.gconstentry.value)

# Safety Imports
from .particle import ParticleWidget