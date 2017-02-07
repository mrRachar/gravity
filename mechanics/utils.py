import math as maths
from numbers import Number

def bearing(x: Number, y: Number) -> float:
    if y == 0:
        return 90
    if y < 0: # or x < 0 > y
        return 180 + maths.degrees(maths.atan(x/y))
    elif x < 0:
        return maths.degrees(maths.atan(x/y)) + 360
    return maths.degrees(maths.atan(x/y))