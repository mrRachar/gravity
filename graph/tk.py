from abc import ABC, abstractmethod

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *

class FigureTk(Figure, Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        Figure.__init__(self)
        self.canvas = FigureCanvasTkAgg(self, master=self)
        self.canvas.get_tk_widget().pack(fill=BOTH)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    @property
    def widget(self):
        return self.canvas.get_tk_widget()

    def drawify(self):
        self.canvas.draw()

class PlayControls(ABC, Frame):
    __is_playing: bool = False

    def __init__(self, master, styling={}, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.play_button = Button(self, text="▶", command=self._play, font=('Consolas', 15), width=2,
                                  **styling
                                  )
        self.play_button.grid(row=0, column=0)

    @abstractmethod
    def play(self): pass

    @abstractmethod
    def pause(self): pass

    def _play(self):
        self.__is_playing ^= True
        if self.is_playing:
            self.play_button['text'] = '■'
            self.play()
        else:
            self.play_button['text'] = "▶"
            self.pause()

    @property
    def is_playing(self) -> bool:
        return self.__is_playing

    @is_playing.setter
    def is_playing(self, value: bool):
        if self.__is_playing == value:
            return
        self.__play()