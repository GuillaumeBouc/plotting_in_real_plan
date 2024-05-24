import numpy as np
from typing import Callable, List
from parametric_curve import ParametricCurve


class PolarCurve:
    def __init__(self, interval_bounds: List[float], r_func: Callable[[float], float]):
        self.interval_bounds = interval_bounds
        self.r_func = r_func

    def to_parametric(self, offset: List[int] = [0, 0]) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            x_func=lambda t: self.r_func(t) * np.cos(t) + offset[0],
            y_func=lambda t: self.r_func(t) * np.sin(t) - offset[1],
        )
