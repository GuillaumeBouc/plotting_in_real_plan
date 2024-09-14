from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class ImageOptions:
    size: Tuple[int, int]
    draw_bounds: Tuple[Tuple[int, int], Tuple[int, int]]
    background_color: Tuple[int, int, int] = (255, 255, 255)
    show_axes: bool = True
    axis_color: Tuple[int, int, int] = (0, 0, 0)
    axis_width: int = 2
    grid_color: Tuple[int, int, int] = (180, 180, 180)
    grid_width: int = 1
    tick_length: int = 15
    name: str = "image"
