from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class ImageOptions:
    image_size: Tuple[int]
    draw_interval_bounds: List[List[int]]
    background_color: Tuple = (255, 255, 255)
    image_name: str = "image"
