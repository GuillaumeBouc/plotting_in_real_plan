import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from color_gradient import GradientGenerator

from options_classes.draw_options import DrawOptions
from options_classes.image_options import ImageOptions
from graphs_classes.parametric_curve import ParametricCurve
from graphs_classes.function_curve import FunctionCurve
from graphs_classes.polar_equation_curve import PolarCurve
from graphs_classes.implicit_function_graph import ImplicitFunctionGraph
from main import main


size = (2048, 2048)
draw_bounds = [[-4, 4], [-4, 4]]

image_options = ImageOptions(
    size=size,
    draw_bounds=draw_bounds,
    show_axes=False,
    background_color=(255, 255, 255),
    name="example",
)

draw_options_per_name = {"example": DrawOptions(1, (0, 0, 0))}
curves_per_name = {
    "example": ImplicitFunctionGraph(
        lambda x, y: int(np.cos(int(x**2)))
        + int(np.cos(int(y**2)))
        + np.tan(x**2 + y**2)
        - np.cos(1.75 * x * y)
        - 0.3,
        lambda x, y: 0,
        ">",
        1e-5,
        draw_bounds,
    )
}

if __name__ == "__main__":
    main(
        curves_per_name,
        image_options,
        draw_options_per_name,
        default_draw_options=DrawOptions(1, (175, 254, 255)),
    )
