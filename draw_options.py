from dataclasses import dataclass
from typing import Tuple


@dataclass
class DrawOptions:
    draw_width: int = 1
    draw_color: Tuple = (0, 0, 0)
