import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from color_gradient import GradientGenerator
from options_classes import DrawOptions, ImageOptions
from graphs_classes import (
    ImplicitFunctionGraph,
    ParametricCurve,
    FunctionCurve,
    PolarCurve,
)
from main import main

size = (1024, 1024)
draw_bounds = [[-4, 4], [-4, 4]]

precision = 1

p_x, p_y = 0, 0
c_x, c_y = 0, 2


def calculate_positions(x, y, i):
    X_p, Y_p = x - p_x - c_x, y - p_y - c_y
    X = ((X_p) * np.cos(np.deg2rad(i)) - (Y_p) * np.sin(np.deg2rad(i))) + c_x
    Y = ((X_p) * np.sin(np.deg2rad(i)) + (Y_p) * np.cos(np.deg2rad(i))) + c_y
    return X, Y


def f(x, y):
    return ((x**2 + y**2) ** 4) - (10 * (x**4 - y**3))


for i, ind in zip(
    np.linspace(0, 360, round(360 / precision)), range(round(360 / precision))
):
    image_options = ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(255, 255, 255),
        name=str(ind),
    )

    draw_options_per_name = {}
    curves_per_name = {}
    f_factory = lambda i: lambda x, y: f(*calculate_positions(x, y, i))

    curves_per_name[f"{ind}_1"] = ImplicitFunctionGraph(
        f_factory(i),
        lambda x, y: 0,
        "=",
        1,
        [[-4, 4], [-4, 4]],
    )
    draw_options_per_name[f"{ind}_1"] = DrawOptions(1, (175, 210, 255))

    if __name__ == "__main__":
        main(
            curves_per_name,
            image_options,
            draw_options_per_name,
            default_draw_options=DrawOptions(1, (175, 254, 255)),
            save_folder="temp/",
        )
