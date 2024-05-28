import numpy as np
from PIL import ImageDraw
from typing import Union

from parametric_curve import ParametricCurve
from implicit_function_graph import ImplicitFunctionGraph
from draw_options import DrawOptions
from my_image import MyImage


class Drawer:
    def __init__(
        self,
        formula: Union[ParametricCurve, ImplicitFunctionGraph],
        draw_options: DrawOptions,
        image: MyImage,
    ) -> None:
        self.formula = formula
        self.draw_options = draw_options
        self.image = image

    def draw(self) -> None:
        if isinstance(self.formula, ParametricCurve):
            self.parametric_curve = self.formula
            self._draw_parametric_curve(self.image.draw)

        elif isinstance(self.formula, ImplicitFunctionGraph):
            self.implicit_function_graph = self.formula
            if self._def_interval_in_draw_interval():
                self._draw_implicit_function_graph(self.image.draw)
            else:
                print("drawer passed")

        else:
            raise ValueError("Invalid formula type")

    def _draw_parametric_curve(self, draw: ImageDraw) -> None:

        t_min, t_max = self.parametric_curve.interval_bounds
        x_func, y_func = self.parametric_curve.x_func, self.parametric_curve.y_func
        x_min, x_max = self.image.image_options.draw_interval_bounds[0]
        y_min, y_max = self.image.image_options.draw_interval_bounds[1]
        scale = (
            self.image.image_options.image_size[0] / (x_max - x_min),
            self.image.image_options.image_size[1] / (y_max - y_min),
        )
        offset = (-x_min * scale[0], -y_min * scale[1])
        print(f"parameter between {t_min} and {t_max}")

        for t in np.linspace(t_min, t_max, self.image.image_options.image_size[0]):
            x = x_func(t)
            y = y_func(t)

            draw.ellipse(
                [
                    (
                        x * scale[0] - self.draw_options.draw_width + offset[0],
                        y * scale[1] - self.draw_options.draw_width + offset[1],
                    ),
                    (
                        x * scale[0] + self.draw_options.draw_width + offset[0],
                        y * scale[1] + self.draw_options.draw_width + offset[1],
                    ),
                ],
                fill=self.draw_options.draw_color,
            )
        return None

    def _draw_implicit_function_graph(self, draw: ImageDraw) -> None:
        x_min, x_max = self.implicit_function_graph.interval_bounds[0]
        y_min, y_max = self.implicit_function_graph.interval_bounds[1]
        image_x_min, image_x_max, image_y_min, image_y_max = (
            self.image.image_options.draw_interval_bounds[0][0],
            self.image.image_options.draw_interval_bounds[0][1],
            self.image.image_options.draw_interval_bounds[1][0],
            self.image.image_options.draw_interval_bounds[1][1],
        )
        scale = (
            (
                (1 / ((image_x_max - image_x_min) / (x_max - x_min)))
                * self.image.image_options.image_size[0]
            )
            / (x_max - x_min),
            (
                (1 / ((image_y_max - image_y_min) / (y_max - y_min)))
                * self.image.image_options.image_size[1]
            )
            / (y_max - y_min),
        )
        offset = (-image_x_min * scale[0], -image_y_min * scale[1])

        x_min, x_max, y_min, y_max = (
            max(x_min, image_x_min),
            min(x_max, image_x_max),
            max(y_min, image_y_min),
            min(y_max, image_y_max),
        )
        print(f"x between {x_min} and {x_max}, y between {y_min} and {y_max}")

        for x in np.linspace(
            x_min,
            x_max,
            round(
                (1 / ((image_x_max - image_x_min) / (x_max - x_min)))
                * self.image.image_options.image_size[0]
            ),
        ):
            for y in np.linspace(
                y_min,
                y_max,
                round(
                    (1 / ((image_x_max - image_x_min) / (x_max - x_min)))
                    * self.image.image_options.image_size[0]
                ),
            ):

                if self.implicit_function_graph.equation(float(x), float(y)):

                    draw.ellipse(
                        [
                            (
                                x * scale[0] - self.draw_options.draw_width + offset[0],
                                y * scale[1] - self.draw_options.draw_width + offset[1],
                            ),
                            (
                                x * scale[0] + self.draw_options.draw_width + offset[0],
                                y * scale[1] + self.draw_options.draw_width + offset[1],
                            ),
                        ],
                        fill=self.draw_options.draw_color,
                    )
        return None

    def _def_interval_in_draw_interval(self) -> bool:
        x_min, x_max = self.implicit_function_graph.interval_bounds[0]
        y_min, y_max = self.implicit_function_graph.interval_bounds[1]
        image_x_min, image_x_max, image_y_min, image_y_max = (
            self.image.image_options.draw_interval_bounds[0][0],
            self.image.image_options.draw_interval_bounds[0][1],
            self.image.image_options.draw_interval_bounds[1][0],
            self.image.image_options.draw_interval_bounds[1][1],
        )

        return any(
            [
                image_x_min <= x_min <= image_x_max
                and image_y_min <= y_min <= image_y_max,
                image_x_min <= x_min <= image_x_max
                and image_y_min <= y_max <= image_y_max,
                image_x_min <= x_max <= image_x_max
                and image_y_min <= y_min <= image_y_max,
                image_x_min <= x_max <= image_x_max
                and image_y_min <= y_max <= image_y_max,
            ]
        )
