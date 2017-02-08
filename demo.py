import matplotlib.animation as animation

from graph import MotionGraphHandler, Animation
from mechanics.particle import *

@Animation()
def simulate(n, graph: MotionGraphHandler, universe: Universe):
    for x in range(int(2e2)):
        universe.tick(n)
    graph.update_positions()
    return [line.line for line in graph.lines]


if __name__ == '__main__':
    universe = Universe([Gravity(6.67408e-11)])
    graph = MotionGraphHandler.create_graph(universe)

    universe <<= Particle(7.342e22, Coords(384.4e6, 0, (384.4e6 * maths.tan(maths.radians(5.14)))), Velocity(1022, 0), colour="grey")
    universe <<= Particle(5.97237e24, Coords(0, 0, 0), Velocity(0, 0), colour="blue")
    graph.ensure_lines()

    graph.axes.set_title('Simulated Lunar Orbit')

    graph.add_animation(simulate)

    graph.axes.set_ylim3d([-5e8,5e8])
    graph.axes.set_xlim3d([-5e8,5e8])
    graph.axes.set_zlim3d([-5e8,5e8])
    graph.show()


if __name__ == '__main__':
    u = Universe([Gravity(6.67408e-11)])
    p1 = Particle(10, Coords(1, 1, 1))
    p2 = Particle(5, Coords(7, 8, 1))
    (u << p1) << p2