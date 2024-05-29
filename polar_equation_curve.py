import numpy as np
from typing import Callable, List
from dataclasses import dataclass

from parametric_curve import ParametricCurve


@dataclass
class PolarCurve:
    interval_bounds: List[float]
    r_func: Callable[[float], float]

    @property
    def to_parametric(self, offset: List[int] = [0, 0]) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            x_func=lambda t: self.r_func(t) * np.cos(t) + offset[0],
            y_func=lambda t: self.r_func(t) * np.sin(t) - offset[1],
        )
