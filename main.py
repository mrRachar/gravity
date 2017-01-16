from graph import FigureTk, MotionGraphHandler
from particle import *
from tkinter import *
from time import sleep

def simulate(handler, window):
    while True:
        sleep(Particle.TICK_LENGTH)
        for particle in handler.particles:
            particle.apply_force(Force(10, Direction(20, 20)))
            particle.tick()
        handler.axes.figure.drawify()
        window.update()


if __name__ == '__main__':
    window = Tk()
    figure = FigureTk(window)
    axes = figure.add_subplot(111, projection='3d')

    #a = axes.plot([5, 3, 2, 3, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    #b = axes.plot([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5])
    #print(a, b)

    figure.grid(row=0, column=0)

    handler = MotionGraphHandler(axes, [Particle(10)])

    print(handler.particle_lines)
    for particle, line in handler.particle_lines.items():
        print(particle, dir(line))

    axes.set_title('Gravitational Motion of Massive Particles')

    play_button = Button(window, text="|>", command=lambda: simulate(handler, window))
    play_button.grid(row=0, column=1)

    mainloop()