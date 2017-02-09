import math as maths
from tkinter import mainloop

from mechanics import Gravity, Universe, Particle, Coords, Velocity
from .interface import GravityWindow
from graph import MotionGraphHandler, Animation


class SimulationAnimation(Animation):
    def step(self, n: int, graph, universe):
        for x in range(int(2e2)):
            universe.tick(n)
        graph.update_positions()


class App:
    universe: Universe
    window: GravityWindow

    def __init__(self):
        self.universe = Universe([Gravity(6.67408e-11)])

    def demo(self):
        self.window = GravityWindow()
        self.axes = self.window.figure.add_subplot(111, projection='3d')
        self.graph = MotionGraphHandler(self.universe, figure=self.window.figure, axes=self.axes)

        self.universe <<= Particle(7.342e22, Coords(384.4e6, 0, (384.4e6 * maths.tan(maths.radians(5.14)))), Velocity(1022, 0), colour="grey")
        self.universe <<= Particle(5.97237e24, Coords(0, 0, 0), Velocity(0, 0), colour="blue")
        self.graph.ensure_lines()

        self.graph.axes.set_title('Simulated Lunar Orbit')
        self.graph.add_animation(SimulationAnimation())

        self.graph.axes.set_ylim3d([-5e8,5e8])
        self.graph.axes.set_xlim3d([-5e8,5e8])
        self.graph.axes.set_zlim3d([-5e8,5e8])
        mainloop()