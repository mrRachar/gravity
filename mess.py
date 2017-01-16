from tkinter import *

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import numpy

window = Tk()

figure = Figure()
axes = figure.add_subplot(111, projection='3d')

a = axes.plot([5, 3, 2, 3, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
b = axes.plot([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5])

print(a, b)

axes.set_title('Gravitational Motion of Massive Particles')

canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack(fill=BOTH)
canvas.mpl_connect('key_press_event', key_press_handler)

axes.mouse_init()

toolbar = NavigationToolbar2TkAgg(canvas, window)
toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

mainloop()