from typing import Tuple

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mechanics.particle import Universe, Particle


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

    def __init__(self, axes, xs=None, ys=None, zs=None, **options):
        self.xs = xs or []
        self.ys = ys or []
        self.zs = zs or []
        self.line = axes.plot(self.xs, self.ys, self.zs, lw=3.5)[0] #, marker='o'
        if options.get("dot") is not False:
            pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(line={self.line}, points={list(self.points)})"

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def add_point(self, x, y, z):
        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)
        self.update()

    def update(self):
        self.line.set_data(self.xs, self.ys)
        self.line.set_3d_properties(self.zs)

    @property
    def points(self):
        return zip(self.xs, self.ys, self.zs)
