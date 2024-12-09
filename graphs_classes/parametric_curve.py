from typing import List, Callable
from dataclasses import dataclass
import torch


@dataclass
class ParametricCurve:
    interval_bounds: List[float]
    draw_interval_bounds: List[List[float]]
    x_func: Callable[[torch.Tensor], torch.Tensor]
    y_func: Callable[[torch.Tensor], torch.Tensor]
    precision: int
