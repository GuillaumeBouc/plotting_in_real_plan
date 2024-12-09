from typing import Callable, List
from dataclasses import dataclass
from pathlib import Path

import torch
import sys

sys.path.append(str(Path(__file__).parent.parent))

from graphs_classes import ParametricCurve


@dataclass
class FunctionCurve:
    interval_bounds: List[float]
    draw_interval_bounds: List[List[float]]
    func: Callable[[torch.Tensor], torch.Tensor]
    precision: int

    def to_parametric(self, offset: List[int] = [0, 0]) -> ParametricCurve:
        return ParametricCurve(
            interval_bounds=self.interval_bounds,
            draw_interval_bounds=self.draw_interval_bounds,
            x_func=lambda t: t + offset[0],
            y_func=lambda t: self.func(t) + offset[1],
            precision=self.precision,
        )
