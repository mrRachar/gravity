from typing import List

from graph import Animation, PlayControls


class SimulationControls(PlayControls):
    animations: List[Animation]

    def __init__(self, master, animations: List[Animation], *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.animations = animations
        self.bind("<space>", lambda x: self._play())

    def play(self):
        for animation in self.animations:
            animation.play()

    def pause(self):
        for animation in self.animations:
            animation.pause()