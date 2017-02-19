from abc import abstractmethod, ABC
from typing import Tuple, List
import math as maths

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

from mechanics.particle import Universe, Particle

class Animation(ABC):
    playing: bool = True

    def __init__(self, interval: int=1, args: Tuple=(), f=None):
        if f:
            self.step = f
        self.interval = 1
        self.args = args

    def __call__(self, f):
        self.step = f
        return self

    def toggle(self) -> bool:
        self.playing ^= True
        return self.playing

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def do(self, *args, **kwargs):
        if self.playing:
            return self.step(*args, **kwargs)

    #@abstractmethod (in trust)
    def step(self, n: int, graph, universe: Universe): pass


class MotionGraphHandler:
    universe: Universe
    axes: Axes3D
    def __init__(self, universe: Universe, figure, axes: Axes3D, plot=None, animations: List[Animation]=None):
        self.universe = universe
        self.plot = plot
        self.figure = figure
        self.axes = axes
        self.particle_lines = {}
        self.animations = animations or []

    @classmethod
    def create_graph(cls, universe: Universe):
        figure = plt.figure()
        axes = figure.add_subplot(111, projection='3d')
        axes.autoscale_view(True, True, True)
        return cls(universe, figure, axes, plt)

    def ensure_lines(self):
        for particle in self.universe.particles:
            if particle not in self.particle_lines:
                self.particle_lines[particle] = Line3DHandler(self.axes, *([n] for n in particle.position),
                                                              colour=particle.colour,
                                                              marker=PointMarker(self.axes,
                                                                                 size=particle.relative_radius*1e-7,
                                                                                 colour=particle.colour
                                                                                 )
                                                              )

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

    def add_animation(self, animation: Animation):
        self.__animation = FuncAnimation(self.figure, animation.do, None, fargs=(self, self.universe) + animation.args,
                                interval=1, blit=False)
        self.animations.append(animation)

    def fit_all(self, coeff=1.2):
        max_outlier = 0
        for particle in self.particles:
            max_outlier = max(max_outlier, abs(particle.position.x), abs(particle.position.x), abs(particle.position.z))
            max_outlier *= coeff
        self.axes.set_ylim3d(-max_outlier, max_outlier)
        self.axes.set_xlim3d(-max_outlier, max_outlier)
        self.axes.set_zlim3d(-max_outlier, max_outlier)


class PointMarker:
    x = 0
    y = 0
    z = 0

    def __init__(self, axes, x=0, y=0, z=0, **options):
        self.x = x
        self.y = y
        self.z = z
        self.line = axes.plot([self.x], [self.y], [self.z],
                              marker=options.get("shape", 'o'),
                              ms=options.get("size", 10),
                              color=options.get("colour", "black")
                              )[0]

    def set_point(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.line.set_data([self.x], [self.y])
        self.line.set_3d_properties([self.z])


class Line3DHandler:
    xs = None
    ys = None
    zs = None
    marker: PointMarker

    def __init__(self, axes, xs=None, ys=None, zs=None, marker=None, colour="black"):
        self.xs = xs or []
        self.ys = ys or []
        self.zs = zs or []
        self.line = axes.plot(self.xs, self.ys, self.zs, color=colour)[0]
        if marker is True:
            marker = PointMarker(axes, self.xs[-1], self.ys[-1], self.zs[-1], colour=colour)
        self.marker = marker

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
        if self.marker:
            self.marker.set_point(self.xs[-1], self.ys[-1], self.zs[-1])

    @property
    def points(self):
        return zip(self.xs, self.ys, self.zs)

    @property
    def colour(self):
        return self.line.get_colour()

    @colour.setter
    def colour(self, value: str):
        self.line.set_color(value)
        self.marker.line.set_color(value)
