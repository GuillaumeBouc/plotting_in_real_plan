import math
from typing import Callable

EasingFunction = Callable[[float], float]


class Easing:
    @staticmethod
    def linear(x: float) -> float:
        return x

    @staticmethod
    def ease_in_cubic(x: float) -> float:
        return x * x * x

    @staticmethod
    def ease_in_out_sine(x: float) -> float:
        return -(math.cos(math.pi * x) - 1) / 2

    @staticmethod
    def ease_in_out_cubic(x: float) -> float:
        if x < 0.5:
            return 4 * x * x * x
        return 1 - pow(-2 * x + 2, 3) / 2
