from tkinter import *
from typing import Tuple


class UserEntry(Frame):
    __label: str = None
    entrylabel: Label = None
    entry: Entry

    def __init__(self, master, label: str = None, **conf):
        super().__init__(master)
        self.__label = label
        if self.label:
            self.entrylabel = Label(self, text=label)
            self.entrylabel.grid(row=0, column=0)
        self.entry = Entry(self, **conf)
        self.entry.pack(row=0, column=1)

    @property
    def value(self) -> str:
        return self.entry.get()

    @value.setter
    def value(self, text: str):
        self.entry['text'] = text

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, text: str):
        self.__label = text
        self.entrylabel['text'] = text


class Vector3DEntry(UserEntry):
    def __init__(self, master, label, **conf):
        super().__init__(master, label)
        self.x = self.entry
        self.y = Entry(self, **conf)
        self.z = Entry(self, **conf)

        self.y.grid(row=0, column=2)
        self.z.grid(row=0, column=3)

    @property
    def value(self) -> Tuple[str, str, str]:
        return (self.x.get(), self.y.get(), self.z.get())

    @value.setter
    def value(self, contents: Tuple[str, str, str]):
        self.x['text'] = contents[0]
        self.y['text'] = contents[1]
        self.z['text'] = contents[2]
