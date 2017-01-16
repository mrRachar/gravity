import math as maths
from abc import ABC, abstractmethod

class Tickable(ABC):
    TICK_LENGTH = 0.1 #seconds

    @abstractmethod
    def tick(self, t: int): pass


class Direction:
    plane = 0   #type: int
    z = 0       #type: int

    def __init__(self, plane=0, z=0):
        self.plane = plane
        self.z = z
        self.normalise()

    @property
    def plane_r(self):
        return maths.radians(self.plane)

    @plane_r.setter
    def plane_r(self, value):
        self.plane_r = maths.degrees(value)

    @property
    def z_r(self):
        return maths.radians(self.z)

    @z_r.setter
    def z_r(self, value):
        self.z_r = maths.degrees(value)

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.__class__.__name__, self.plane, self.z)

    def __neg__(self):
        value = self.__class__(self.plane + 180, self.z + 360)
        value.normalise()
        return value

    def __pos__(self):
        value = self.__class__(self.plane, self.z)
        value.normalise()
        return value

    def normalise(self):
        while self.plane > 360:
            self.plane -= 360
        while self.plane < 0:
            self.plane += 360

        while self.z > 360:
            self.z -= 360
        while self.z < 0:
            self.z += 360


class Vector3D:
    magnitude = 0                   #type: int
    direction = Direction(0, 0)     #type: Direction

    def __init__(self, magnitude: int, direction: (Direction, int)):
        self.magnitude = magnitude
        if isinstance(direction, int):
            direction = Direction()
        self.direction = direction
        
    def __add__(self, other):
        return self._apply(lambda x,y: x+y,  other)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        return self._apply(lambda x,y: x*y,  other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self._apply(lambda x,y: x/y,  other)

    def __mod__(self, other):
        return self._apply(lambda x,y: x%y,  other)

    def __sub__(self, other):
        return self._apply(lambda x,y: x-y,  other)

    def __neg__(self):
        return self.__class__(self.magnitude, -self.direction)

    def __bool__(self) -> bool:
        return not not self.magnitude

    def _apply(self, op, other):
        x, y, z = self.components
        if not isinstance(other, Vector3D):
            x = op(x, other)
            y = op(y, other)
            z = op(z, other)
        else:
            x_o, y_o, z_o = other.components
            x = op(x, x_o)
            y = op(y, y_o)
            z = op(z, z_o)
        return self.__class__.from_components(x, y, z)

    @property
    def components(self):
        x = maths.cos(self.direction.plane_r) * maths.cos(self.direction.z_r) * self.magnitude
        y = maths.sin(self.direction.plane_r) * maths.cos(self.direction.z_r) * self.magnitude
        z = maths.sin(self.direction.z_r) * self.magnitude
        return x, y, z

    @classmethod
    def from_components(cls, x, y, z):
        planar_magnitude = maths.sqrt(x**2 + y**2)
        magnitude = maths.sqrt(planar_magnitude**2 + z**2)
        #maths.sqrt(sum(n**2 for n in xyz))
        direction = Direction()
        if planar_magnitude:
            direction.plane = maths.degrees(maths.acos(x / planar_magnitude))
        if magnitude:
            direction.z = maths.degrees(maths.asin(z / magnitude))
        return cls(magnitude, direction)

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.__class__.__name__, self.magnitude, self.direction)


class Displacement(Vector3D): pass

class Velocity(Vector3D):
    def to_displacement(self, time: (int, float)):
        return Displacement(self.magnitude * time, +self.direction)

class Acceleration(Vector3D):
    def to_velocity(self, time: (int, float)):
        return Velocity(self.magnitude * time, +self.direction)

    def to_force(self, mass: int):
        return Force(self.magnitude * mass, +self.direction)

    def to_displacement(self, time: (int, float)):
        return Displacement(0.5 * self.magnitude * pow(time, 2), +self.direction)

class Force(Vector3D):
    def to_acceleration(self, mass: int):
        return Acceleration(self.magnitude / mass, +self.direction)


class Coords:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_from(self, other):
        return maths.sqrt(sum(map(lambda x: x**2, (self.x - other.x, self.y - other.y, self.z - other.z))))

    @property
    def components(self) -> tuple:
        return self.x, self.y, self.z

    def __iter__(self):
        yield from self.components

    def __add__(self, displacement):
        d_x, d_y, d_z = displacement.components
        return self.__class__(self.x + d_x, self.y + d_y, self.z + d_z)

    def __repr__(self) -> str:
        return "{}({}, {}, {})".format(self.__class__.__name__, self.x, self.y, self.z)


class Particle(Tickable):
    mass = 0
    position = Coords(0, 0, 0)
    velocity = Velocity(0, 0)
    acceleration = Acceleration(0, 0)

    def __init__(self, mass=0, position=None, velocity=None, acceleration=None):
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
