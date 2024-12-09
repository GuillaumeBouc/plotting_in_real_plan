import torch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from options_classes import DrawOptions, ImageOptions
from graphs_classes import ImplicitFunctionGraphFactory, ImplicitFunctionGraph
from make_animation import make_animation

size = (512, 512)
draw_bounds = [[-8, 8], [-8, 8]]

p_x, p_y = 0, 0
c_x, c_y = 0, -1


def calculate_rotations(x, y, i):
    X_p, Y_p = x - p_x - c_x, y - p_y - c_y
    angle_rad = torch.deg2rad(torch.tensor(i, dtype=x.dtype))
    cos_theta = torch.cos(angle_rad)
    sin_theta = torch.sin(angle_rad)
    X = ((X_p) * cos_theta - (Y_p) * sin_theta) + c_x
    Y = ((X_p) * sin_theta + (Y_p) * cos_theta) + c_y
    return X, Y


def f1(x, y):
    return (
        torch.arctan(2 * torch.cos(x) ** 2 + 2 * torch.sin(y) ** 2)
        + torch.sin(y)
        - torch.sin(x)
        - 2 * torch.cos(x**2 + y**2)
    )


def f2(x, y):
    return (
        torch.arctan(2 * torch.cos(x) ** 2 + 2 * torch.sin(y) ** 2)
        - torch.sin(y)
        + torch.sin(x)
        - 2 * torch.cos(x**2 + y**2)
    )


def f3(x, y):
    return torch.maximum(f1(x, y), f2(x, y))


make_animation(
    [0, 360],
    360,
    [
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: f1(*calculate_rotations(t_x, t_y, p)),
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: f2(*calculate_rotations(t_x, t_y, p)),
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: f3(*calculate_rotations(t_x, t_y, p)),
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
    "results/animations/implicit_function_graph_rotation_example.avi",
    resolution=(512, 512),
    FPS=120,
)
