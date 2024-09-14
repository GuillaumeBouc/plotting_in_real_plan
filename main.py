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


def create_parametric_curve(interval, x_func, y_func):
    return ParametricCurve(
        interval_bounds=interval,
        draw_interval_bounds=[[-15, 15], [-15, 15]],
        x_func=x_func,
        y_func=y_func,
    )


def main():
    image_options = ImageOptions(
        size=(4000, 4000),
        draw_bounds=[[-15, 15], [-15, 15]],
        background_color=(255, 255, 255),
        show_axes=True,
    )

    image = MyImage(options=image_options)

    default_draw_options = DrawOptions(draw_color=(120, 160, 240), line_width=5)

    curves = {
        "background": ImplicitFunctionGraph(
            left_term=lambda x, y: np.sin(x - np.sin(x + y)),
            right_term=lambda x, y: 0,
            sign="=",
            tolerance=1e-2,
            interval_bounds=[[-15, 15], [-15, 15]],
        ),
        "star": create_parametric_curve(
            [0, 6 * np.pi],
            lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3) + 7.5,
            lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3) + 7.5,
        ),
        "heart": create_parametric_curve(
            [0, 6 * np.pi],
            lambda t: (8 * np.cos(t) - 6 * np.cos(8 * t / 3)) / 2 - 7.5,
            lambda t: (8 * np.sin(t) - 6 * np.sin(8 * t / 3)) / 2 - 7.5,
        ),
        "sine_wave": FunctionCurve(
            interval_bounds=[-15, 0],
            draw_interval_bounds=[[-15, 15], [-15, 15]],
            func=lambda x: x + 15 + 2 * np.sin(3 * x) + 2 * np.cos(2 * x),
        ).to_parametric,
        "spiral": PolarCurve([0, 4 * np.pi], r_func=lambda t: 0.5 * t).to_parametric(
            offset=[7.5, 7.5], draw_interval_bounds=[[-15, 15], [-15, 15]]
        ),
    }

    custom_draw_options = {
        "background": DrawOptions(draw_color=(200, 240, 240), line_width=5),
        "star": DrawOptions(draw_color=(100, 160, 240), line_width=5),
        "heart": DrawOptions(draw_color=(160, 160, 240), line_width=5),
    }

    drawers = [
        Drawer(curve, custom_draw_options.get(name, default_draw_options), image, name)
        for name, curve in curves.items()
    ]

    for index, drawer in enumerate(drawers, 1):
        print(f"Drawer {drawer.name} (n°{index}) started")
        draw_timer = timeit.Timer(lambda: drawer.draw())
        print(
            f"Drawer {drawer.name} (n°{index}) took: {draw_timer.timeit(1):.6f} seconds\n"
        )

    image.image.transpose(Image.FLIP_TOP_BOTTOM).save(f"image/{image.name}.png")


if __name__ == "__main__":
    main()
