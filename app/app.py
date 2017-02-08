from mechanics import Gravity, Universe
from .interface import GravityWindow


class App:
    universe: Universe
    window: GravityWindow

    def __init__(self):
        self.universe = Universe([Gravity(6.67408e-11)])

    def run(self):
        self.window = GravityWindow()
