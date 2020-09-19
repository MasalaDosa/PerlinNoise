import random
from math import pi, floor

from vector import Vector


class Noise:
    DEFAUT_SIZE = 256

    def __init__(self, size = DEFAUT_SIZE):
        self.size = size
        self.permutations = self._build_permutations()
        self.gradients = self._build_gradients()

    def _get_permutation_index(self, x, y):
        return self.permutations[(self.permutations[x % self.size] + y) % self.size]

    def get(self, x, y):
        x_floor = floor(x)
        y_floor = floor(y)

        xf = x - x_floor
        yf = y - y_floor

        top_right = Vector(xf - 1.0, yf - 1.0)
        top_left = Vector(xf, yf - 1.0)
        bottom_right = Vector(xf - 1.0, yf)
        bottom_left = Vector(xf, yf)

        grad_top_right = self.gradients[self._get_permutation_index(x_floor + 1, y_floor + 1)]
        grad_top_left = self.gradients[self._get_permutation_index(x_floor, y_floor + 1)]
        grad_bottom_right = self.gradients[self._get_permutation_index(x_floor + 1, y_floor)]
        grad_bottom_left = self.gradients[self._get_permutation_index(x_floor, y_floor)]

        dot_top_right = top_right.dot(grad_top_right)
        dot_top_left = top_left.dot(grad_top_left)
        dot_bottom_right = bottom_right.dot(grad_bottom_right)
        dot_bottom_left = bottom_left.dot(grad_bottom_left)

        u = Noise._fade(xf)
        v = Noise._fade(yf)

        return Noise._lerp(
            u,
            Noise._lerp(v, dot_bottom_left, dot_top_left),
            Noise._lerp(v, dot_bottom_right, dot_top_right)
        )

    def get_with_octaves(self, x, y, num_octaves):
        noise = 0.0
        amplitude = 1.0
        frequency = 1.0
        maxi = 0.0
        for i in range(num_octaves):
            noise += self.get(frequency * x, frequency * y) * amplitude
            maxi += amplitude
            frequency *= 2.0
            amplitude /= 2.0
        return noise / maxi

    def _build_permutations(self):
        ps = list(range(0, self.size))
        random.shuffle(ps)
        return ps

    def _build_gradients(self):
        gs = []
        for i in range(0, self.size):
            gradient = Vector.from_theta(random.uniform(0, 2 * pi))
            gs.append(gradient)
        return gs

    @staticmethod
    def _fade(t):
        return ((6 * t - 15) * t + 10) * t * t * t

    @staticmethod
    def _lerp(t, a1, a2):
        return a1 + t * (a2 - a1)
