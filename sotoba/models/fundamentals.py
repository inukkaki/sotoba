from __future__ import annotations
import math


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

    def __iadd__(self, other: Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vector) -> Vector:
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector(new_x, new_y)

    def __isub__(self, other: Vector) -> Vector:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar: float) -> Vector:
        new_x = self.x * scalar
        new_y = self.y * scalar
        return Vector(new_x, new_y)

    def __rmul__(self, scalar: float) -> Vector:
        new_x = scalar * self.x
        new_y = scalar * self.y
        return Vector(new_x, new_y)

    def __imul__(self, scalar: float) -> Vector:
        self.x *= scalar
        self.y *= scalar
        return self

    def __truediv__(self, scalar: float) -> Vector:
        new_x = self.x / scalar
        new_y = self.y / scalar
        return Vector(new_x, new_y)

    def __itruediv__(self, scalar: float) -> Vector:
        self.x /= scalar
        self.y /= scalar
        return self

    def __floordiv__(self, scalar: float) -> Vector:
        new_x = self.x // scalar
        new_y = self.y // scalar
        return Vector(new_x, new_y)

    def __ifloordiv__(self, scalar: float) -> Vector:
        self.x //= scalar
        self.y //= scalar
        return self

    def __neg__(self) -> Vector:
        new_x = -self.x
        new_y = -self.y
        return Vector(new_x, new_y)

    def __pos__(self) -> Vector:
        new_x = +self.x
        new_y = +self.y
        return Vector(new_x, new_y)

    def assign(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
