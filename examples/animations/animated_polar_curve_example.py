import torch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from options_classes import DrawOptions, ImageOptions
from graphs_classes import PolarCurve, PolarCurveFactory
from make_animation import make_animation


size = (512, 512)
draw_bounds = [[-4, 4], [-4, 4]]


make_animation(
    [0, 50 * torch.pi],
    100,
    [
        PolarCurveFactory(
            lambda p: PolarCurve(
                [0, 0 + p],
                draw_bounds,
                lambda r: 3 * torch.sin((24 * r) / 25),
                precision=20000,
            )
        ),
    ],
    [
        DrawOptions(1, (255, 34, 118)),
    ],
    ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(0, 0, 0),
    ),
    "results/animations/animated_polar_curve_example.avi",
    resolution=(512, 512),
)
