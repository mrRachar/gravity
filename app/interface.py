from tkinter import *
import math as maths

import matplotlib.animation as animation

from mechanics import *
from graph import *

class SimulationAnimation(Animation): pass

class SimulationControls(PlayControls):
    def __init__(self, master, animation, *args, **kwargs):
        super().__init__(self, master, *args, **kwargs)
        self.animation = animation

    def play(self):
        self.animation.play()

    def pause(self):
        self.animation.stop()

class GravityWindow(Tk):
    figure: FigureTk

    def __init__(self, animation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figure = FigureTk(self)
        self.figure.grid(0, 0)
        self.controls = SimulationControls(self, animation)
        self.controls.grid(col=1, row=0)


def simulate(n, tickable: Tickable, graph: MotionGraphHandler):
    for x in range(int(2e2)):
        tickable.tick(n)
    graph.update_positions()
    return [line.line for line in graph.lines]

if __name__ == '__main__':

    window = Tk()
    g_i = FigureTk(window)
    g_i.pack()
    axes = g_i.canvas.figure.add_subplot(111, projection='3d')
    graph = MotionGraphHandler(universe, None, g_i.canvas.figure, axes)

    universe <<= Particle(7.342e22, Coords(384.4e6, 0, (384.4e6 * maths.tan(maths.radians(5.14)))), Velocity(1022, 0), colour="grey")
    universe <<= Particle(5.97237e24, Coords(0, 0, 0), Velocity(0, 0), colour="blue")
    graph.ensure_lines()

    graph.axes.set_title('Simulated Lunar Orbit')

    line_ani = animation.FuncAnimation(graph.figure, simulate, None, fargs=(universe, graph,),
                                       interval=1, blit=False)

    graph.axes.set_ylim3d([-5e8,5e8])
    graph.axes.set_xlim3d([-5e8,5e8])
    graph.axes.set_zlim3d([-5e8,5e8])
    #graph.show()