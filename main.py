import matplotlib.animation as animation

from graph import MotionGraphHandler
from mechanics.particle import *


def simulate(n, tickable: Tickable, graph: MotionGraphHandler):
    tickable.tick(n)
    graph.update_positions()
    print(n, graph.lines)
    return [graph.lines]


if __name__ == '__main__':
    universe = Universe([Gravity(6.67408e-11)])
    graph = MotionGraphHandler.create_graph(universe)

    universe <<= Particle(10, Coords(1, 2, 2))
    universe <<= Particle(5, Coords(5, 5, 1))
    graph.ensure_lines()

    graph.axes.set_title('Gravitational Motion of Massive Particles')

    line_ani = animation.FuncAnimation(graph.figure, simulate, None, fargs=(universe, graph,),
                                       interval=50, blit=False)

    graph.axes.set_ylim3d([-10,10])
    graph.axes.set_xlim3d([-10,10])
    graph.axes.set_zlim3d([-10,10])
    graph.show()


if __name__ == '__main__':
    u = Universe([Gravity(6.67408e-11)])
    p1 = Particle(10, Coords(1, 1, 1))
    p2 = Particle(5, Coords(7, 8, 1))
    (u << p1) << p2