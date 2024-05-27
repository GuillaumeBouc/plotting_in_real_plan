import numpy as np
import timeit
from PIL import Image

from my_image import MyImage
from image_options import ImageOptions
from draw_options import DrawOptions
from drawer import Drawer
from parametric_curve import ParametricCurve
from function_curve import FunctionCurve
from polar_equation_curve import PolarCurve
from implicit_equation_graph import ImplicitEquationGraph


def main():
    image_options = ImageOptions(
        image_size=(4000, 4000),
        draw_interval_bounds=[[-15, 15], [-15, 15]],
        background_color=(255, 255, 255),
        has_axis=True,
    )

    image = MyImage(image_options)

    draw_options_and_parametric_curve_per_name = {
        "background": [
            ImplicitEquationGraph(
                left_term=lambda x, y: np.sin(x - np.sin(x + y)),
                rigth_term=lambda x, y: 0,
                sign="=",
                tolerance=1e-2,
                interval_bounds=[[-15, 15], [-15, 15]],
            ),
            DrawOptions(draw_color=(200, 240, 240), draw_width=10),
        ],
        "star": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                x_func=lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3) + 7.5,
                y_func=lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3) + 7.5,
            ),
            DrawOptions(draw_color=(100, 160, 240), draw_width=20),
        ],
        "heart": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                x_func=lambda t: (8 * np.cos(t) - 6 * np.cos(8 * t / 3)) / 2 - 7.5,
                y_func=lambda t: (8 * np.sin(t) - 6 * np.sin(8 * t / 3)) / 2 - 7.5,
            ),
            DrawOptions(draw_color=(160, 160, 240), draw_width=20),
        ],
        "some_func": [
            FunctionCurve(
                interval_bounds=[-15, 0],
                func=lambda x: x + 15 + 2 * np.sin(3 * x) + 2 * np.cos(2 * x),
            ).to_parametric(),
            DrawOptions(draw_color=(60, 120, 240), draw_width=20),
        ],
        "spiral": [
            ParametricCurve(
                interval_bounds=[0, 4 * np.pi],
                x_func=lambda t: 0.5 * t * np.cos(t) + 8 + np.cos(t),
                y_func=lambda t: 0.5 * t * np.sin(t) - 8 + np.cos(t),
            ),
            DrawOptions(draw_color=(120, 120, 240), draw_width=20),
        ],
    }

    drawers = [
        Drawer(parametric, draw_option, image)
        for parametric, draw_option in draw_options_and_parametric_curve_per_name.values()
    ]

    for drawer in drawers:
        print(f"Drawer n°{drawers.index(drawer)} started")
        timer = timeit.Timer(lambda: drawer.draw())
        print(
            f"Drawer n°{drawers.index(drawer)} took: {timer.timeit(1):.6f} seconds",
            "\n",
        )
    image.image.transpose(Image.FLIP_TOP_BOTTOM).save(f"image/{image.name}.png")


if __name__ == "__main__":
    main()
