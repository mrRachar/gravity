from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from typing import Tuple

from particle import Universe, Particle

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import *

class FigureTk(Figure):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = Frame(master)
        self.canvas = FigureCanvasTkAgg(self, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=BOTH)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    @property
    def widget(self):
        return self.canvas.get_tk_widget()

    def pack(self, *args, **kwargs): self.frame.pack(*args, **kwargs)
    def grid(self, *args, **kwargs): self.frame.grid(*args, **kwargs)
    def grid_forget(self): self.frame.grid_forget()

    def drawify(self):
        self.canvas.draw()


class MotionGraphHandler:
    universe: Universe
    axes: Axes3D
    def __init__(self, universe: Universe, plot, figure, axes: Axes3D):
        self.universe = universe
        self.plot = plot
        self.figure = figure
        self.axes = axes
        self.particle_lines = {}

    @classmethod
    def create_graph(cls, universe: Universe):
        figure = plt.figure()
        axes = figure.add_subplot(111, projection='3d')
        axes.autoscale_view(True, True, True)
        return cls(universe, plt, figure, axes)

    def ensure_lines(self):
        for particle in self.universe.particles:
            if particle not in self.particle_lines:
                self.particle_lines[particle] = Line3DHandler(self.axes, *([n] for n in particle.position))

    @property
    def particles(self) -> Tuple[Particle, ...]:
        return tuple(self.particle_lines.keys())

    @property
    def lines(self):
        lines: Tuple[Line3DHandler] = tuple(self.particle_lines.values())
        return lines


    def update_positions(self):
        for particle, line in self.particle_lines.items():
            line.add_point(*particle.position)

    def show(self):
        self.plot.show()


class Line3DHandler:
    xs = None
    ys = None
    zs = None

    def __init__(self, axes, xs=None, ys=None, zs=None):
        self.xs = xs or []
        self.ys = ys or []
        self.zs = zs or []
        self.line = axes.plot(self.xs, self.ys, self.zs)[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(line={self.line}, points={list(self.points)})"

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def add_point(self, x, y, z):
        self.xs.append(x)
        self.ys.append(x)
        self.zs.append(x)
        self.update()

    def update(self):
        self.line.set_data(self.xs, self.ys)
        self.line.set_3d_properties(self.zs)

    @property
    def points(self):
        return zip(self.xs, self.ys, self.zs)
