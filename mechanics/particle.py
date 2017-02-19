from abc import ABC, abstractmethod
from typing import Optional, List
import copy

from .vectors import *


class Tickable(ABC):
    TICK_LENGTH = 100 #seconds

    @abstractmethod
    def tick(self, t: int): pass

class Copyable(ABC):
    @abstractmethod
    def copy(self): pass

class Particle(Tickable, Copyable):
    mass: Number = 0
    position: Coords = Coords(0, 0, 0)
    velocity: Velocity = Velocity(0, 0)
    acceleration: Acceleration = Acceleration(0, 0)
    colour: str
    __name: str

    def __init__(self, name: str, mass: Number, position: Coords=None, velocity: Velocity=None, acceleration: Acceleration=None, colour: str="black"):
        self.name = name
        self.mass = mass
        if position is not None:
            self.position = position
        if velocity is not None:
            self.velocity = velocity
        if acceleration is not None:
            self.acceleration = acceleration
        self.colour = colour

    def tick(self, t: int=0): #tick number later?
        # ut + 1/2a(t^2)
        self.position += self.velocity.to_displacement(self.TICK_LENGTH) + self.acceleration.to_displacement(self.TICK_LENGTH)
        self.velocity += self.acceleration.to_velocity(self.TICK_LENGTH)
        self.acceleration = Acceleration(0, 0)

    def apply_force(self, force: Force):
        self.acceleration += force.to_acceleration(self.mass)

    def __repr__(self) -> str:
        return "{}({!r}, {}, {}, {}, {})".format(self.__class__.__name__, self.name, self.mass, self.position, self.velocity, self.acceleration)

    @property
    def relative_radius(self):
        return pow((3 * self.mass)/(4 * maths.pi), 1/3)

    def copy(self):
        return self.__class__(self.name, self.mass, copy.copy(self.position), copy.copy(self.velocity), copy.copy(self.acceleration), self.colour)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value.title()


class Field(Copyable, ABC):
    @abstractmethod
    def apply(self, universe): pass

    def copy(self):
        return self

class Gravity(Field):
    G: Number

    def __init__(self, G: Number):
        self.G = G

    def apply(self, universe):
        for particle in universe.particles:
            for other in universe.particles:
                if other is particle:
                    continue
                #print(particle, other, self.calculate_force(particle, other))
                particle.apply_force(self.calculate_force(particle, other))
                #print(particle)

    def calculate_force(self, subject: Particle, actor: Particle) -> Force:
        force = Force(0, 0)
        force.direction = subject.position.direction_to(actor.position)
        force.magnitude = self.G * ((subject.mass * actor.mass)/pow(subject.position.distance_to(actor.position),2))
        #print(force)
        return force

    def copy(self):
        return self.__class__(self.G)


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

    def copy(self):
        return Universe(
            fields=[field.copy() for field in self.fields],
            particles=[particle.copy() for particle in self.particles]
        )

