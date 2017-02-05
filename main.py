import matplotlib.animation as animation

from graph import MotionGraphHandler
from mechanics.particle import *


def simulate(n, tickable: Tickable, graph: MotionGraphHandler):
    universe.tick(n)
    graph.update_positions()
    print(n, graph.lines)
    return [graph.lines]


if __name__ == '__main__':
    universe = Universe([Gravity(6.67408e-11)])
    graph = MotionGraphHandler.create_graph(universe)

    universe <<= Particle(10, Coords(10, 5, 10))
    universe <<= Particle(5, Coords(-10, -10, -10))
    graph.ensure_lines()

    graph.axes.set_title('Gravitational Motion of Massive Particles')

    line_ani = animation.FuncAnimation(graph.figure, simulate, None, fargs=(universe, graph,),
                                       interval=50, blit=False)

    graph.show()



"""if __name__ == '__old__':
    graph = MotionGraphHandler.create_graph()

    particle = Particle(10, Coords(5, 5, 5))

    graph.add_particle(particle)
    line = graph.lines[0]

    graph.axes.set_title('Gravitational Motion of Massive Particles')

    line_ani = animation.FuncAnimation(graph.figure, simulate, None, fargs=(particle, line,),
                                       interval=50, blit=False)


    graph.show()
"""