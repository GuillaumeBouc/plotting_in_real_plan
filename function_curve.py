from typing import Callable, List
from dataclasses import dataclass
from parametric_curve import ParametricCurve


@dataclass
class FunctionCurve:
    interval_bounds: List[float]
    draw_interval_bounds: List[List[float]]
    func: Callable[[float], float]

    @property
    def to_parametric(self) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            draw_interval_bounds=self.draw_interval_bounds,
            x_func=lambda t: t,
            y_func=lambda t: self.func(t),
        )
