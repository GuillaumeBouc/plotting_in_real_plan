from typing import Dict, Union
import timeit
import torch

from canvas import Canvas
from drawer import Drawer
from options_classes import ImageOptions, DrawOptions
from graphs_classes import ParametricCurve, ImplicitFunctionGraph


def main(
    curves: Dict[str, Union[ParametricCurve, ImplicitFunctionGraph]],
    image_options: ImageOptions,
    draw_options: Dict[str, DrawOptions],
    default_draw_options: DrawOptions = DrawOptions(1, (0, 0, 0)),
    device: torch.device = torch.device("cpu"),
) -> Canvas:

    image = Canvas(
        options=image_options,
    )

    drawers = [
        Drawer(curve, draw_options.get(name, default_draw_options), image, name)
        for name, curve in curves.items()
    ]

    for index, drawer in enumerate(drawers, 1):
        print(f"Drawer {drawer.name} (n°{index}) started")
        draw_timer = timeit.Timer(lambda: drawer.draw(device))
        print(
            f"Drawer {drawer.name} (n°{index}) took: {draw_timer.timeit(1):.6f} seconds\n"
        )

    return image
