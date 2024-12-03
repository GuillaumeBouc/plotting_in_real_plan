import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from options_classes import DrawOptions, ImageOptions
from graphs_classes import FunctionCurve, FunctionCurveFactory
from make_animation import make_animation


size = (1024, 1024)
draw_bounds = [[-8, 8], [-8, 8]]

make_animation(
    [0, 16],
    200,
    [
        FunctionCurveFactory(
            lambda p: FunctionCurve(
                [-8, -8 + p], [[-8, 8], [-8, 8]], lambda x: np.sin(x)
            )
        ),
    ],
    [
        DrawOptions(10, (120, 190, 235)),
    ],
    ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(255, 255, 255),
    ),
    "results/animations/animated_function_curve_example.avi",
    resolution=(1024, 1024),
)
