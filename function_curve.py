from typing import Callable, List
from parametric_curve import ParametricCurve


class FunctionCurve:
    def __init__(
        self,
        interval_bounds: List[float],
        func: Callable[[float], float],
    ):
        self.interval_bounds = interval_bounds
        self.func = func

    def to_parametric(self) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            x_func=lambda t: t,
            y_func=lambda t: self.func(t),
        )
