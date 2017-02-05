from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import *

import numpy

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
    def __init__(self, figure, axes: Axes3D):
        self.figure = figure
        self.axes = axes
        self.particles = []
        self.lines = []

    @classmethod
    def create_graph(cls):
        figure = plt.figure()
        axes = figure.add_subplot(111, projection='3d')
        return cls(figure, axes)

    def add_particle(self, particle):
        self.particles.append(particle)
        self.lines.append(self.axes.plot([n] fparticle.c]))

class LineData:
    xs = None
    ys = None
    zs = None

    def __init__(self, xs: list, ys: list, zs: list):
        self.xs = xs
        self.ys = ys
        self.zs = zs

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def append(self, x, y, z):
        self.xs.append(x)
        self.ys.append(x)
        self.zs.append(x)

    @property
    def points(self):
        return zip(self.xs, self.ys, self.zs)
