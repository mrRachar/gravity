from mechanics import Universe


class Experiment:
    name: str
    universe: Universe = None
    speed: int = 200

    def __init__(self, name: str, universe: Universe=None):
        self.name = name
        self.universe = universe or Universe()