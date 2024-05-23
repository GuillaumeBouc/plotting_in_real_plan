from typing import Callable, List
from dataclasses import dataclass


@dataclass
class ParametricCurve:
    interval_bounds: List[float]
    x_func: Callable[[float], float]
    y_func: Callable[[float], float]
