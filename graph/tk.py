from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *

class FigureTk(Figure):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = Frame(master)
        self.canvas = FigureCanvasTkAgg(self, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=BOTH)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    @property
    def widget(self):
        return self.canvas.get_tk_widget()

    def pack(self, *args, **kwargs): self.frame.pack(*args, **kwargs)
    def grid(self, *args, **kwargs): self.frame.grid(*args, **kwargs)
    def grid_forget(self): self.frame.grid_forget()

    def drawify(self):
        self.canvas.draw()