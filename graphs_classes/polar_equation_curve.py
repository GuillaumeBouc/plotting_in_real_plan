import numpy as np
from typing import Callable, List
from dataclasses import dataclass

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from graphs_classes.parametric_curve import ParametricCurve


@dataclass
class PolarCurve:
    interval_bounds: List[float]
    draw_interval_bounds: List[List[float]]
    r_func: Callable[[float], float]
    precision: int

    def to_parametric(
        self,
        offset: List[int] = [0, 0],
    ) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            draw_interval_bounds=self.draw_interval_bounds,
            x_func=lambda t: self.r_func(t) * np.cos(t) + offset[0],
            y_func=lambda t: self.r_func(t) * np.sin(t) - offset[1],
            precision=self.precision,
        )
