from dataclasses import dataclass
from typing import Tuple


@dataclass
class DrawOption:
    draw_width: int = 1
    draw_color: Tuple = (0, 0, 0)
