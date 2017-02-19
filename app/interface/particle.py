from tkinter import *
from tkinter.colorchooser import askcolor
from typing import List, Dict, Any, Union

from graph import Line3DHandler, MotionGraphHandler
from app.experiment import Experiment
from mechanics import Gravity, Universe, Particle, Velocity, Coords
from .input import ResetableUserEntry, ResetableVector3DEntry

class ParticleWidget(Frame):
    colour_view: Frame
    title: Union[Label, ResetableUserEntry]
    mass: Union[Label, ResetableUserEntry]
    velocity: Union[Label, ResetableVector3DEntry]
    position: Union[Label, ResetableVector3DEntry]
    tail: Union[Label, ResetableUserEntry]
    buttons: Frame
    apply_button: Button
    test_button: Button
    reset_button: Button
    cancel_button: Button

    universe_particle: Particle
    experiment_particle: Particle
    line: Line3DHandler
    experiment_universe: Universe
    universe: Universe
    simulation: MotionGraphHandler

    __edit_mode: bool = False

    _mass_format = "{:1.1f} kg"
    _velocity_format = "{:4.1f} ∠ {:3.2f}, {:2.2f} ms⁻¹"
    _position_format = "{:=+12.0f}, {:=+12.0f}, {:=+12.0f}"

    def __init__(self, master, experiment_universe: Universe, universe: Universe, simulation: MotionGraphHandler,
                 experiment_particle: Particle, universe_particle: Particle, line: Line3DHandler,
                 buttonconf: Dict[str, Any]=None,
                 entryconf: Dict[str, Any]=None,
                 labelconf: Dict[str, Any]=None,
                 specialbuttonconf: Dict[str, Any]=None,
                 *args, **kwargs):
        self.frameconf = kwargs.copy()
        if 'bd' not in kwargs:
            kwargs['bd'] = 2
        if 'relief' not in kwargs:
            kwargs['relief'] = 'groove'
        super().__init__(master, *args, **kwargs)

        self.universe_particle = universe_particle
        self.experiment_particle = experiment_particle
        self.line = line
        self.experiment_universe = experiment_universe
        self.universe = universe
        self.simulation = simulation

        self.buttonconf = buttonconf or {}
        self.entryconf = entryconf or {}
        self.specialbuttonconf = specialbuttonconf or {}
        self.labelconf = labelconf or {}
        self.value_labelconf = {
            'font': ('Consolas', '9'),
            **labelconf
        }
        self.title_labelconf = {
            'font': ('Arial', '12'),
            **labelconf
        }


        self.colour_view: Frame = Frame(self, bg=universe_particle.colour, height=15, width=15)
        self.title: Union[Label, ResetableUserEntry] = Label(self, text=universe_particle.name, **self.title_labelconf)
        self.mass: Union[Label, ResetableUserEntry] = Label(self, text=self._mass_format.format(universe_particle.mass), **self.value_labelconf)
        self.velocity: Union[Label, ResetableVector3DEntry] = Label(self, text=self._velocity_format.format(universe_particle.velocity.magnitude,
                                                                                                    *universe_particle.velocity.direction),
                                                                                                    **self.value_labelconf
                                                                                                    )
        self.position: Union[Label, ResetableVector3DEntry] = Label(self,
                                                                    text=self._position_format.format(*universe_particle.position),
                                                                    **self.value_labelconf
                                                                    )
        self.buttons = SimpleListPane(self, start_from=RIGHT, packconfig={'padx': 3}, **self.frameconf)
        self.buttons.append(Button(self.buttons, text='Edit', command=self.enable_edit, **self.specialbuttonconf))
        self.buttons.append(Button(self.buttons, text='Delete', command=self.delete, **self.buttonconf))


        self.grid_all_default()

    def update(self):
        if not self.__edit_mode:
            self.velocity['text'] = self._velocity_format.format(
                self.universe_particle.velocity.magnitude,
                *self.universe_particle.velocity.direction
            )
            self.position['text'] = self._position_format.format(*self.universe_particle.position)

    @property
    def value_widgets(self):
        yield self.colour_view
        yield self.title
        yield self.mass
        yield self.position
        yield self.velocity

    def forget_all(self):
        for child in self.value_widgets:
            child.grid_forget()
        self.buttons.clear()
        self.buttons.grid_forget()

    def grid_all_default(self):
        self.colour_view.grid(row=0, column=0, sticky=E, padx=5)
        self.title.grid(row=0, column=1, sticky=W)
        self.mass.grid(row=1, column=0, columnspan=2)
        self.velocity.grid(row=3, column=0, columnspan=2)
        self.position.grid(row=2, column=0, columnspan=2)
        self.buttons.grid(row=4, column=0, columnspan=2, sticky=E)

    def reset_all(self):
        for child in self.value_widgets:
            try:
                child.onreset()
            except AttributeError:
                continue

    def enable_edit(self):
        self.__edit_mode = True
        self.forget_all()

        self.colour_view = Frame(self, bg=self.universe_particle.colour, width=15, height=15)
        self.colour_view.bind("<Button-1>", self.colour_choose)

        titleentrystyle = {
            'entryconf': {**self.entryconf, 'font': ('Arial', 12), 'justify': CENTER},
            'labelconf': self.labelconf,
            'buttonconf': self.buttonconf,
            **self.frameconf
        }
        userentrystyle = {
            'entryconf': self.entryconf,
            'labelconf': self.labelconf,
            'buttonconf': self.buttonconf,
            **self.frameconf
        }
        vectorentrystyle = {
            'entryconf': {'width': 10, **self.entryconf},
            'labelconf': self.labelconf,
            'buttonconf': self.buttonconf,
            **self.frameconf
        }
        self.title = ResetableUserEntry(self, "", lambda *_: self.experiment_particle.name, **titleentrystyle)
        self.mass = ResetableUserEntry(self, "Mass", lambda *_: str(self.experiment_particle.mass), **userentrystyle)
        self.velocity = ResetableVector3DEntry(self, "Velocity",
                                               lambda *_: tuple(f"{c:1.1f}" for c in self.experiment_particle.velocity.components),
                                               **vectorentrystyle
                                               )
        self.position = ResetableVector3DEntry(self, "Coordinates",
                                               lambda *_: tuple(f"{c:1.1f}" for c in self.experiment_particle.position.components),
                                               **vectorentrystyle
                                               )
        self.buttons.append(Button(self.buttons, text='Apply', command=self.apply_values, **self.specialbuttonconf))
        self.buttons.append(Button(self.buttons, text='Test', command=self.test_values, **self.buttonconf))
        self.buttons.append(Button(self.buttons, text='Reset', command=self.reset_all, **self.buttonconf))
        self.buttons.append(Button(self.buttons, text='Return', command=self.enable_view, **self.specialbuttonconf))

        self.title.value = self.universe_particle.name
        self.mass.value = self.universe_particle.mass
        self.velocity.value = tuple(f"{c:1.1f}" for c in self.universe_particle.velocity.components)
        self.position.value = tuple(f"{c:1.1f}" for c in self.universe_particle.position.components)

        self.grid_all_default()

    def colour_choose(self, *_):
        self.colour_view['bg'] = askcolor(self.colour_view['bg'])[1]

    def test_values(self):
        self.universe_particle.name = self.title.value
        self.universe_particle.velocity = Velocity.from_components(*(float(c) for c in self.velocity.value))
        self.universe_particle.colour = self.colour_view['bg']
        self.universe_particle.mass = float(self.mass.value)
        self.universe_particle.position = Coords(*(float(c) for c in self.position.value))
        self.line.colour = self.colour_view['bg']

    def apply_values(self):
        self.test_values()
        self.experiment_particle.name = self.title.value
        self.experiment_particle.velocity = Velocity.from_components(*(float(c) for c in self.velocity.value))
        self.experiment_particle.colour = self.colour_view['bg']
        self.experiment_particle.mass = float(self.mass.value)
        self.experiment_particle.position = Coords(*(float(c) for c in self.position.value))

    def enable_view(self):
        self.__edit_mode = False
        self.forget_all()

        self.colour_view: Frame = Frame(self, bg=self.universe_particle.colour, height=15, width=15)
        self.title: Union[Label, ResetableUserEntry] = Label(self, text=self.universe_particle.name, **self.title_labelconf)
        self.mass: Union[Label, ResetableUserEntry] = Label(self, text=self._mass_format.format(self.universe_particle.mass), **self.value_labelconf)
        self.velocity: Union[Label, ResetableVector3DEntry] = Label(self, text=self._velocity_format.format(self.universe_particle.velocity.magnitude,
                                                                                                            *self.universe_particle.velocity.direction),
                                                                    **self.value_labelconf
                                                                    )
        self.position: Union[Label, ResetableVector3DEntry] = Label(self,
                                                                    text=self._position_format.format(*self.universe_particle.position),
                                                                    **self.value_labelconf
                                                                    )
        self.buttons = SimpleListPane(self, start_from=RIGHT, packconfig={'padx': 3}, **self.frameconf)
        self.buttons.append(Button(self.buttons, text='Edit', command=self.enable_edit, **self.specialbuttonconf))
        self.buttons.append(Button(self.buttons, text='Delete', command=self.delete, **self.buttonconf))

        self.grid_all_default()

    def delete(self):
        self.universe.particles.remove(self.universe_particle)
        self.experiment_universe.particles.remove(self.experiment_particle)
        self.simulation.particle_lines.pop(self.universe_particle)
        self.line.xs = self.line.xs[-1:]
        self.line.ys = self.line.ys[-1:]
        self.line.zs = self.line.zs[-1:]
        self.pack_forget()
        self.line.update()



# Safety Imports
from app.interface.pane import SimpleListPane