import math as maths
from numbers import Number

from .bearing import bearing

class Direction:
    plane: Number
    z: Number

    def __init__(self, plane: Number=0, z: Number=0):
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
    magnitude: Number
    direction: Direction

    def __init__(self, magnitude: Number, direction: (Direction, Number)):
        self.magnitude = magnitude
        if isinstance(direction, Number):
            direction = Direction(direction)
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
        x = maths.sin(self.direction.plane_r) * maths.cos(self.direction.z_r) * self.magnitude
        y = maths.cos(self.direction.plane_r) * maths.cos(self.direction.z_r) * self.magnitude
        z = maths.sin(self.direction.z_r) * self.magnitude
        return x, y, z

    @classmethod
    def from_components(cls, x, y, z):
        planar_magnitude = maths.sqrt(x**2 + y**2)
        magnitude = maths.sqrt(planar_magnitude**2 + z**2)
        #maths.sqrt(sum(n**2 for n in xyz))
        direction = Direction()
        if planar_magnitude:
            #direction.plane = maths.degrees(maths.acos(y / planar_magnitude))
            direction.plane = bearing(x, y)
        if magnitude:
            direction.z = bearing(-z, planar_magnitude)
        return cls(magnitude, direction)

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.__class__.__name__, self.magnitude, self.direction)


class Displacement(Vector3D): pass

class Velocity(Vector3D):
    def to_displacement(self, time: Number) -> Displacement:
        return Displacement(self.magnitude * time, +self.direction)

class Acceleration(Vector3D):
    def to_velocity(self, time: Number) -> Velocity:
        return Velocity(self.magnitude * time, +self.direction)

    def to_force(self, mass: Number):
        return Force(self.magnitude * mass, +self.direction)

    def to_displacement(self, time: Number, u: Velocity=Velocity(0,0)) -> Displacement:
        return u.to_displacement(time) + Displacement(0.5 * self.magnitude * pow(time, 2), +self.direction)

class Force(Vector3D):
    def to_acceleration(self, mass: Number) -> Acceleration:
        return Acceleration(self.magnitude / mass, +self.direction)


class Coords:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other) -> Number:
        return maths.sqrt(sum(map(lambda x: x**2, (self.x - other.x, self.y - other.y, self.z - other.z))))

    def direction_to(self, other) -> Direction:
        return (other.to_displacement() - self.to_displacement()).direction

    def to_displacement(self) -> Displacement:
        return Displacement.from_components(*self.components)

    @classmethod
    def from_displacement(cls, displacement):
        return cls(*displacement.components)

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