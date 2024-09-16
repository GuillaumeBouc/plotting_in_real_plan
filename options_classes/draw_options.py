from dataclasses import dataclass
from typing import Tuple


@dataclass
class DrawOptions:
    line_width: int = 1
    draw_color: Tuple[int] = (0, 0, 0)  ## RGB
