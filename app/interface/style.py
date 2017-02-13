from typing import Callable, Dict, Union

window_styling = {
    'bg': "#4f4f4f",
}
widget_styling = {
    'bg': "#444444",
    'fg': "#eeeeee",
    'relief': "groove",
}
graph_styling = {
    'bg': '#efefef'
}

class Style:
    text = "#eeeeee"
    background = "#4f4f4f"

    button_background = "#444444"
    button_text = "#eeeeee"
    button_relief = "groove"
    button_active_background = "#707070"
    button_active_text = "#cfcfcf"
    button_padx = 2
    button_pady = 2

    special_button_text = "#ffffff"
    special_button_background = "#5555c0"
    special_button_active_background = "#0D58FF"
    special_button_active_text = "#ffffff"

    entry_background = "white"
    entry_relief = "flat"
    entry_text = "black"

    graph_background = "#efefef"

    @staticmethod
    def attributes():
        for attribute, value in Style.__dict__.items():
            if not attribute.startswith('_') and not isinstance(value, Callable):
                return attribute

    @classmethod
    def from_dict(cls, source: Dict[str, Union[str, int]]):
        instance = cls()
        for attribute in cls.attributes():
            try:
                setattr(instance, attribute, source[attribute])
            except KeyError:
                continue
        return instance

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {attribute: getattr(self, attribute) for attribute in self.attributes()}

    @property
    def button_format(self) -> Dict[str, Union[str, int]]:
        return {
            'fg': self.button_text,
            'bg': self.button_background,
            'relief': self.button_relief,
            'activebackground': self.button_active_background,
            'activeforeground': self.button_active_text,
            'padx': self.button_padx,
            'pady': self.button_pady
        }

    @property
    def special_button_format(self) -> Dict[str, Union[str, int]]:
        return {
            'fg': self.special_button_text,
            'bg': self.special_button_background,
            'relief': self.button_relief,
            'activebackground': self.special_button_active_background,
            'activeforeground': self.special_button_active_text,
            'padx': self.button_padx,
            'pady': self.button_pady
        }

    @property
    def label_format(self) -> Dict[str, Union[str, int]]:
        return self.text_format

    @property
    def text_format(self) -> Dict[str, Union[str, int]]:
        return {
            'fg': self.text,
            'bg': self.background,
        }

    @property
    def frame_format(self):
        return {
            'bg': self.background
        }

    @property
    def entry_format(self) -> Dict[str, Union[str, int]]:
        return {
            'fg': self.entry_text,
            'bg': self.entry_background,
            'relief': self.entry_relief
        }