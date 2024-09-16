import numpy as np

from options_classes.draw_options import DrawOptions
from options_classes.image_options import ImageOptions
from graphs_classes.parametric_curve import ParametricCurve
from graphs_classes.function_curve import FunctionCurve
from graphs_classes.polar_equation_curve import PolarCurve
from graphs_classes.implicit_function_graph import ImplicitFunctionGraph
from main import main

size = (4000, 4000)
draw_bounds = [[-15, 15], [-15, 15]]

image_options = ImageOptions(
    size=size,
    draw_bounds=draw_bounds,
    name="exemple_1",
)

curves_per_name = {
    "background": ImplicitFunctionGraph(
        left_term=lambda x, y: np.sin(x - np.sin(x + y)),
        right_term=lambda x, y: 0,
        sign="=",
        tolerance=1e-2,
        interval_bounds=draw_bounds,
    ),
    "star": ParametricCurve(
        [0, 6 * np.pi],
        draw_bounds,
        lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3) + 7.5,
        lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3) + 7.5,
    ),
    "heart": ParametricCurve(
        [0, 6 * np.pi],
        draw_bounds,
        lambda t: (8 * np.cos(t) - 6 * np.cos(8 * t / 3)) / 2 - 7.5,
        lambda t: (8 * np.sin(t) - 6 * np.sin(8 * t / 3)) / 2 - 7.5,
    ),
    "sine_wave": FunctionCurve(
        interval_bounds=[-15, 0],
        draw_interval_bounds=draw_bounds,
        func=lambda x: x + 2 * np.sin(3 * x) + 2 * np.cos(2 * x),
    ).to_parametric(offset=[0, 15]),
    "spiral": PolarCurve(
        interval_bounds=[0, 4 * np.pi],
        draw_interval_bounds=[[-15, 15], [-15, 15]],
        r_func=lambda t: 0.5 * t,
    ).to_parametric(offset=[7.5, 7.5]),
}

draw_options_per_name = {"background": DrawOptions(5, (220, 70, 40))}
if __name__ == "__main__":
    main(
        curves_per_name,
        image_options,
        draw_options_per_name,
        default_draw_options=DrawOptions(10, (70, 70, 200)),
    )
