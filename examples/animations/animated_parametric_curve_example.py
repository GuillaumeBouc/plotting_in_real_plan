import sys
import torch
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from options_classes import DrawOptions, ImageOptions
from graphs_classes import ParametricCurve, ParametricCurveFactory
from make_animation import make_animation


size = (512, 512)
draw_bounds = [[-15, 15], [-15, 15]]


make_animation(
    [0, 6 * torch.pi],
    100,
    [
        ParametricCurveFactory(
            lambda p: ParametricCurve(
                [0, 0 + p],
                draw_bounds,
                x_func=lambda x: 8 * torch.cos(x) - 6 * torch.cos((8 * x) / 3),
                y_func=lambda y: 8 * torch.sin(y) - 6 * torch.sin((8 * y) / 3),
                precision=5000,
            )
        ),
    ],
    [
        DrawOptions(1, (33, 225, 255)),
    ],
    ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(0, 0, 0),
    ),
    "results/animations/animated_parametric_curve_example.avi",
    resolution=(512, 512),
)
