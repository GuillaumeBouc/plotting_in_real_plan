import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from options_classes import DrawOptions, ImageOptions
from graphs_classes import ImplicitFunctionGraphFactory, ImplicitFunctionGraph
from make_animation import make_animation

size = (128, 128)
draw_bounds = [[-8, 8], [-8, 8]]

p_x, p_y = 0, 0
c_x, c_y = 0, -1


def calculate_rotations(x, y, i):
    X_p, Y_p = x - p_x - c_x, y - p_y - c_y
    X = ((X_p) * np.cos(np.deg2rad(i)) - (Y_p) * np.sin(np.deg2rad(i))) + c_x
    Y = ((X_p) * np.sin(np.deg2rad(i)) + (Y_p) * np.cos(np.deg2rad(i))) + c_y
    return X, Y


def f1(x, y):
    return (
        np.arctan(2 * np.cos(x) ** 2 + 2 * np.sin(y) ** 2)
        + np.sin(y)
        - np.sin(x)
        - 2 * np.cos(x**2 + y**2)
    )


def f2(x, y):
    return (
        np.arctan(2 * np.cos(x) ** 2 + 2 * np.sin(y) ** 2)
        - np.sin(y)
        + np.sin(x)
        - 2 * np.cos(x**2 + y**2)
    )


def f3(x, y):
    return max(f1(x, y), f2(x, y))


make_animation(
    [0, 360],
    360,
    [
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda x, y: f1(*calculate_rotations(x, y, p)),
                lambda x, y: 0,
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda x, y: f2(*calculate_rotations(x, y, p)),
                lambda x, y: 0,
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda x, y: f3(*calculate_rotations(x, y, p)),
                lambda x, y: 0,
                "<",
                10e-5,
                draw_bounds,
            )
        ),
    ],
    [
        DrawOptions(1, (120, 190, 235)),
        DrawOptions(1, (220, 235, 105)),
        DrawOptions(1, (235, 130, 120)),
    ],
    ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(255, 255, 255),
    ),
    "results/animations/implicit_function_grap_rotation_example.avi",
    resolution=(128, 128),
)
