import torch
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

size = (4096, 4096)
draw_bounds = [[-4, 4], [-4, 4]]

image_options = ImageOptions(
    size=size,
    draw_bounds=draw_bounds,
    show_axes=False,
    background_color=(255, 255, 255),
    name="implicit_example",
)

draw_options_per_name = {"implicit_example": DrawOptions(1, (0, 0, 0))}
curves_per_name = {
    "implicit_example": ImplicitFunctionGraph(
        lambda x, y: torch.floor(torch.cos(torch.floor(x**2)))
        + torch.floor(torch.cos(torch.floor(y**2)))
        + torch.tan(x**2 + y**2)
        - torch.cos(1.75 * x * y)
        - 0.3,
        ">",
        1e-10,
        draw_bounds,
    )
}

if __name__ == "__main__":
    main(
        curves_per_name,
        image_options,
        draw_options_per_name,
        default_draw_options=DrawOptions(1, (0, 0, 0)),
    ).save(f"results/images/{image_options.name}.png")
