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
from implicit_function_graph import ImplicitFunctionGraph


def main():
    image_options = ImageOptions(
        image_size=(4000, 4000),
        draw_interval_bounds=[[-15, 15], [-15, 15]],
        background_color=(255, 255, 255),
        has_axis=True,
    )

    image = MyImage(image_options)

    draw_options_and_graph_per_name = {
        "background": [
            None,
            ImplicitFunctionGraph(
                left_term=lambda x, y: np.sin(x - np.sin(x + y)),
                rigth_term=lambda x, y: 0,
                sign="=",
                tolerance=1e-2,
                interval_bounds=[[-15, 15], [-15, 15]],
            ),
            DrawOptions(draw_color=(200, 240, 240), line_width=10),
        ],
        "star": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                draw_interval_bounds=[[-15, 15], [-15, 15]],
                x_func=lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3) + 7.5,
                y_func=lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3) + 7.5,
            ),
            None,
            DrawOptions(draw_color=(100, 160, 240), line_width=20),
        ],
        "heart": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                draw_interval_bounds=[[-15, 15], [-15, 15]],
                x_func=lambda t: (8 * np.cos(t) - 6 * np.cos(8 * t / 3)) / 2 - 7.5,
                y_func=lambda t: (8 * np.sin(t) - 6 * np.sin(8 * t / 3)) / 2 - 7.5,
            ),
            None,
            DrawOptions(draw_color=(160, 160, 240), line_width=20),
        ],
        "some_func": [
            FunctionCurve(
                interval_bounds=[-15, 0],
                draw_interval_bounds=[[-15, 15], [-15, 15]],
                func=lambda x: x + 15 + 2 * np.sin(3 * x) + 2 * np.cos(2 * x),
            ).to_parametric,
            None,
            DrawOptions(draw_color=(60, 120, 240), line_width=20),
        ],
        "spiral": [
            PolarCurve([0, 4 * np.pi], r_func=lambda t: 0.5 * t).to_parametric(
                offset=[7.5, 7.5], draw_interval_bounds=[[-15, 15], [-15, 15]]
            ),
            None,
            DrawOptions(draw_color=(120, 120, 240), line_width=20),
        ],
    }

    drawers = [
        Drawer(parametric, implicit, draw_option, image, name)
        for name, (
            parametric,
            implicit,
            draw_option,
        ) in draw_options_and_graph_per_name.items()
    ]

    for drawer in drawers:
        print(f"Drawer {drawer.name} (n°{drawers.index(drawer)}) started")
        timer = timeit.Timer(lambda: drawer.draw())
        print(
            f"Drawer {drawer.name} (n°{drawers.index(drawer)}) took: {timer.timeit(1):.6f} seconds",
            "\n",
        )
    image.image.transpose(Image.FLIP_TOP_BOTTOM).save(f"image/{image.name}.png")


if __name__ == "__main__":
    main()
