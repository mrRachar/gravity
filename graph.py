from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
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
    def __init__(self, axes: Axes3D, particles: list, *args, **kwargs):
        self.axes = axes
        self.particles = particles
        self.particle_lines = {particle: self.axes.plot(*([n] for n in particle.position.components))[0] for particle in particles}

    def update_positions(self):
        for particle in self.particles:
            LineUtils.append_point(self.particle_lines[particle], particle.position)
        self.axes.figure.draw(self.axes)  #figure.draw()


class LineUtils:
    @staticmethod
    def append_point(line, *points):
        for point in points:
            x, y, z = point
            #x_data, y_data, z_data = line.get_xdata(), line.get_ydata(), line.get_zdata()
            line.set_xdata(numpy.append(line.get_xdata(), x))
            line.set_ydata(numpy.append(line.get_ydata(), y))
            line.set_zorder(numpy.append(line.get_zdata(), z))