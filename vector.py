from math import sqrt, sin, cos


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    @staticmethod
    def from_theta(theta):
        x = sin(theta)
        y = cos(theta)
        return Vector(x, y)
