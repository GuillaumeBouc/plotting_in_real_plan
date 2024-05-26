import numpy as np
from PIL import ImageDraw
from typing import Union

from parametric_curve import ParametricCurve
from implicit_equation_graph import ImplicitEquationGraph
from draw_options import DrawOptions
from my_image import MyImage


class Drawer:
    def __init__(
        self,
        formula: Union[ParametricCurve, ImplicitEquationGraph],
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

        elif isinstance(self.formula, ImplicitEquationGraph):
            self.implicit_equation_graph = self.formula
            self._draw_implicit_equation_graph(self.image.draw)

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

    def _draw_implicit_equation_graph(self, draw: ImageDraw) -> None:
        x_min, x_max = self.implicit_equation_graph.interval_bounds[0]
        y_min, y_max = self.implicit_equation_graph.interval_bounds[1]
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

                if self.implicit_equation_graph.equation(float(x), float(y)):

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
