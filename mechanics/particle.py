from abc import ABC, abstractmethod
from typing import Optional, List

from .vectors import *


class Tickable(ABC):
    TICK_LENGTH = 0.1 #seconds

    @abstractmethod
    def tick(self, t: int): pass

class Particle(Tickable):
    mass: Number = 0
    position: Coords = Coords(0, 0, 0)
    velocity: Velocity = Velocity(0, 0)
    acceleration: Acceleration = Acceleration(0, 0)

    def __init__(self, mass: Number, position: Coords=None, velocity: Velocity=None, acceleration: Acceleration=None):
        self.mass = mass
        if position is not None:
            self.position = position
        if velocity is not None:
            self.velocity = velocity
        if acceleration is not None:
            self.acceleration = acceleration

    def tick(self, t: int=0): #tick number later?
        # ut + 1/2a(t^2)
        self.position += self.velocity.to_displacement(self.TICK_LENGTH) + self.acceleration.to_displacement(self.TICK_LENGTH)
        self.velocity = self.acceleration.to_velocity(self.TICK_LENGTH)
        self.acceleration = Acceleration(0, 0)

    def apply_force(self, force: Force):
        self.acceleration += force.to_acceleration(self.mass)

    def __repr__(self) -> str:
        return "{}({}, {}, {}, {})".format(self.__class__.__name__, self.mass, self.position, self.velocity, self.acceleration)


class Field(ABC):
    @abstractmethod
    def apply(self, universe): pass

class Gravity(Field):
    G: Number

    def __init__(self, G: Number):
        self.G = G

    def apply(self, universe):
        for particle in universe.particles:
            for other in universe.particles:
                if other is particle:
                    continue
                particle.apply_force(self.calculate_force(particle, other))

    def calculate_force(self, subject: Particle, actor: Particle) -> Force:
        force = Force(0, 0)
        force.direction = subject.position.direction_to(actor.position)
        force.magnitude = self.G * ((subject.mass * actor.mass)/pow(subject.position.distance_to(actor.position),2))
        print(force)
        return force


class Universe(Tickable):
    particles: List[Particle]
    fields: List[Field]

    def __init__(self, fields: Optional[List[Field]]=None, particles: Optional[List[Particle]]=None):
        self.fields = fields or []
        self.particles = particles or []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def __lshift__(self, particle: Particle):
        self.add_particle(particle)
        return self

    def tick(self, t: int=0):
        for field in self.fields:
            field.apply(self)

        for particle in self.particles:
            particle.tick(t)

