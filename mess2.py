import matplotlib.animation as animation
import matplotlib.pyplot as plt

from mechanics.particle import *

data = [[] for _ in range(3)]

def simulate(n, particle, lines):
    global data
    particle.apply_force(Force(10, Direction(20, 20)))
    particle.tick()
    append(data, *particle.position)
    print(data, lines[0])
    lines[0].set_data(data[0], data[1])
    lines[0].set_3d_properties(data[2])
    return lines
        
def append(list_, x, y, z):
    list_[0].append(x)
    list_[1].append(x)
    list_[2].append(x)

figure = plt.figure()
axes = figure.add_subplot(111, projection='3d')

particle = Particle(10, Coords(0, 0, 0))
append(data, *particle.position)

#print(a, b)

lines = axes.plot(*data)

axes.set_title('Gravitational Motion of Massive Particles')

line_ani = animation.FuncAnimation(figure, simulate, None, fargs=(particle, lines,),
                                   interval=50, blit=False)


plt.show()
