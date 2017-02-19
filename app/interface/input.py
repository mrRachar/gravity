from tkinter import *
from typing import Tuple, Callable, Dict, Any


class EntryField(Entry):
    placeholder_active: bool = False
    placeholder: str
    placeholder_colour: str

    def __init__(self, master, placeholder: str="", placeholder_colour: str="#aaaaaa", fg='black', text="", *args, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_colour = placeholder_colour
        self.text_colour = fg
        self.value = text

        self.bind("<FocusIn>", self.on_focus)
        self.bind("<FocusOut>", self.on_leave)

    def set(self, text: str):
        self.delete(0, END)
        self.insert(0, text)

    @property
    def value(self) -> str:
        if self.placeholder_active:
            return ""
        return super().get()

    @value.setter
    def value(self, content: str):
        if content == "":
            self.enable_placeholder()
        else:
            self.disable_placeholder()
            self.set(content)

    def get(self):
        return self.value

    def enable_placeholder(self):
        if not self.placeholder_active:
            self['fg'] = self.placeholder_colour
            self.placeholder_active = True
            self.set(self.placeholder)

    def disable_placeholder(self):
        if self.placeholder_active:
            self['fg'] = self.text_colour
            self.set("")
            self.placeholder_active = False

    def on_focus(self, event):
        if self.placeholder_active:
            self.disable_placeholder()

    def on_leave(self, event):
        if not self.value:
            self.enable_placeholder()


class UserEntry(Frame):
    __label: str = None
    entrylabel: Label = None
    entry: Entry

    def __init__(self, master, label: str=None, placeholder="", entryconf=None, labelconf=None, **conf):
        super().__init__(master, **conf)
        self.__label = label
        if self.label:
            self.entrylabel = Label(self, text=label, padx=5, **(labelconf or {}))
            self.entrylabel.pack(side=LEFT, anchor=W)
        self.entry = EntryField(self, placeholder=placeholder, **(entryconf or {}))
        self.entry.pack(anchor=E)

    @property
    def value(self) -> str:
        return self.entry.get()

    @value.setter
    def value(self, text: str):
        self.entry.value = text

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, text: str):
        self.__label = text
        self.entrylabel['text'] = text

    def set(self, *value):
        if len(value) == 1:
            value = value[0]
        self.value = value


class Vector3DEntry(UserEntry):
    def __init__(self, master, label, entryconf: Dict[str, Any]=None, labelconf: Dict[str, Any]=None, **conf):
        labelconf = labelconf or {}
        entryconf = {
            'width': 4,
            **(entryconf or {}),
            'justify': RIGHT
        }
        super().__init__(master, label,
                         entryconf=entryconf,
                         labelconf=labelconf,
                         placeholder=" z",
                         **conf
                         )
        self.z = self.entry
        self.y = EntryField(self, placeholder=' y', **entryconf)
        self.x = EntryField(self, placeholder=' x', **entryconf)
        self.z.config(**entryconf)

        self.z.pack_configure(padx=2)
        self.y.pack(side=RIGHT, padx=20)
        self.x.pack(side=RIGHT, padx=2)

    @property
    def value(self) -> Tuple[str, str, str]:
        return (self.x.get(), self.y.get(), self.z.get())

    @value.setter
    def value(self, contents: Tuple[str, str, str]):
        self.x.value = contents[0]
        self.y.value = contents[1]
        self.z.value = contents[2]


class ResetableUserEntry(UserEntry):
    def __init__(self, master, label: str, resetfunc: Callable[[UserEntry, str], str], buttonconf=None, *args, **kwargs):
        super().__init__(master, label, *args, **kwargs)
        buttonconf = (buttonconf or {}).copy()
        buttonconf.update({
            'width': 2,
            'height': 1,
            'padx': 0,
            'pady': 0,
        })
        self.resetfunc = resetfunc
        self.resetbutton = Button(self, text="⟳", command=self.onreset, **buttonconf)
        self.resetbutton.pack(side=RIGHT, padx=2)
        self.entry['width'] = int(self.entry['width'] - 6)
        self.entry.pack_forget()
        self.entry.pack(side=RIGHT)

    def onreset(self):
        result = self.resetfunc(self, self.value)
        if isinstance(result, str):
            self.value = result

class ResetableVector3DEntry(ResetableUserEntry, Vector3DEntry):
    def __init__(self, master, label: str, resetfunc: Callable[[UserEntry, Tuple[str, str, str]], Tuple[str, str, str]], buttonconf=None, *args, **kwargs):
        Vector3DEntry.__init__(self, master, label, *args, **kwargs)
        buttonconf = (buttonconf or {}).copy()
        buttonconf.update({
            'width': 2,
            'height': 1,
            'padx': 0,
            'pady': 0,
        })
        self.resetfunc = resetfunc
        self.resetbutton = Button(self, text="⟳", command=self.onreset, **buttonconf)
        self.resetbutton.pack(side=RIGHT, padx=2)
        self.entry['width'] = int(self.entry['width'] - 6)
        self.z.pack_forget()
        self.z.pack(side=RIGHT)
        self.y.pack_forget()
        self.y.pack(side=RIGHT)
        self.x.pack_forget()
        self.x.pack(side=RIGHT)

    def onreset(self):
        result = self.resetfunc(self, self.value)
        if isinstance(result, tuple):
            self.value = result