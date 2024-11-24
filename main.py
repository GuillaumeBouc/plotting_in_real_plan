import timeit
from typing import Dict, Union
from PIL import Image

from canvas import Canvas
from options_classes.image_options import ImageOptions
from options_classes.draw_options import DrawOptions
from drawer import Drawer
from graphs_classes.parametric_curve import ParametricCurve
from graphs_classes.implicit_function_graph import ImplicitFunctionGraph


def main(
    curves: Dict[str, Union[ParametricCurve, ImplicitFunctionGraph]],
    image_options: ImageOptions,
    draw_options: Dict[str, DrawOptions],
    default_draw_options: DrawOptions = DrawOptions(1, (0, 0, 0)),
    save_folder: str = "results/images/",
):

    image = Canvas(
        options=image_options,
    )

    drawers = [
        Drawer(curve, draw_options.get(name, default_draw_options), image, name)
        for name, curve in curves.items()
    ]

    for index, drawer in enumerate(drawers, 1):
        print(f"Drawer {drawer.name} (n°{index}) started")
        draw_timer = timeit.Timer(lambda: drawer.draw())
        print(
            f"Drawer {drawer.name} (n°{index}) took: {draw_timer.timeit(1):.6f} seconds\n"
        )

    image.image.transpose(Image.FLIP_TOP_BOTTOM).save(f"{save_folder}{image.name}.png")
