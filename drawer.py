import numpy as np
from PIL import ImageDraw
from typing import Tuple

from parametric_curve import ParametricCurve
from implicit_function_graph import ImplicitFunctionGraph
from draw_options import DrawOptions
from my_image import MyImage


class Drawer:
    def __init__(
        self,
        parametric_curve: ParametricCurve = None,
        implicit_function_graph: ImplicitFunctionGraph = None,
        draw_options: DrawOptions = None,
        image: MyImage = None,
        name: str = None,
    ) -> None:
        self.parametric_curve = parametric_curve
        self.implicit_function_graph = implicit_function_graph

        if parametric_curve is not None:
            self.formula = parametric_curve
        elif implicit_function_graph is not None:
            self.formula = implicit_function_graph
        else:
            raise ValueError(
                "Drawer must have a parametric curve or an implicit function graph but not both"
            )
        self.draw_options = draw_options
        self.image = image
        self.name = name

    def draw(self) -> None:
        self.image_bounds = (
            self.image.image_options.draw_interval_bounds[0][0],
            self.image.image_options.draw_interval_bounds[0][1],
            self.image.image_options.draw_interval_bounds[1][0],
            self.image.image_options.draw_interval_bounds[1][1],
        )

        match self.formula:
            case self.parametric_curve:
                self.bounds = (
                    self.parametric_curve.draw_interval_bounds[0][0],
                    self.parametric_curve.draw_interval_bounds[0][1],
                    self.parametric_curve.draw_interval_bounds[1][0],
                    self.parametric_curve.draw_interval_bounds[1][1],
                )
                self.parameter_bounds = self.parametric_curve.interval_bounds
                self._draw_parametric_curve(self.image.draw)
            case self.implicit_function_graph:
                self.bounds = (
                    self.implicit_function_graph.interval_bounds[0][0],
                    self.implicit_function_graph.interval_bounds[0][1],
                    self.implicit_function_graph.interval_bounds[1][0],
                    self.implicit_function_graph.interval_bounds[1][1],
                )
                if self._definition_interval_in_draw_interval():
                    self._draw_implicit_function_graph(self.image.draw)
            case _:
                raise ValueError(
                    "The definition interval of the implicit function graph is not in the draw interval"
                )

    def _draw_parametric_curve(self, draw: ImageDraw) -> None:

        t_min, t_max = self.parameter_bounds
        x_func, y_func = self.parametric_curve.x_func, self.parametric_curve.y_func

        image_x_min, image_x_max, image_y_min, image_y_max = self.image_bounds
        scale = self._calculate_scale()
        offset = (-image_x_min * scale[0], -image_y_min * scale[1])
        print(f"parameter between {t_min} and {t_max}")

        for t in np.linspace(t_min, t_max, self.image.image_options.image_size[0]):
            x = x_func(t)
            y = y_func(t)

            self._draw_ellipse(x, y, draw, scale, offset)

        return None

    def _draw_implicit_function_graph(self, draw: ImageDraw) -> None:

        def_x_min, def_x_max, def_y_min, def_y_max = self.bounds
        image_x_min, image_x_max, image_y_min, image_y_max = self.image_bounds

        intersect = self._intersect_draw_interval_image_size()
        scale = self._calculate_scale()
        offset = (-image_x_min * scale[0], -image_y_min * scale[1])

        x_min, x_max, y_min, y_max = (
            max(def_x_min, image_x_min),
            min(def_x_max, image_x_max),
            max(def_y_min, image_y_min),
            min(def_y_max, image_y_max),
        )
        print(f"x between {x_min} and {x_max}, y between {y_min} and {y_max}")

        for x in np.linspace(
            x_min,
            x_max,
            round(intersect[0]),
        ):
            for y in np.linspace(
                y_min,
                y_max,
                round(intersect[1]),
            ):

                if self.implicit_function_graph.equation(float(x), float(y)):
                    self._draw_ellipse(x, y, draw, scale, offset)
        return None

    def _definition_interval_in_draw_interval(self) -> bool:
        def_x_min, def_x_max, def_y_min, def_y_max = self.bounds
        image_x_min, image_x_max, image_y_min, image_y_max = self.image_bounds
        return any(
            [
                image_x_min <= def_x_min <= image_x_max
                and image_y_min <= def_y_min <= image_y_max,
                image_x_min <= def_x_min <= image_x_max
                and image_y_min <= def_y_max <= image_y_max,
                image_x_min <= def_x_max <= image_x_max
                and image_y_min <= def_y_min <= image_y_max,
                image_x_min <= def_x_max <= image_x_max
                and image_y_min <= def_y_max <= image_y_max,
            ]
        )

    def _draw_ellipse(
        self, x: float, y: float, draw: ImageDraw, scale: Tuple[int], offset: Tuple[int]
    ) -> None:
        draw.ellipse(
            [
                (
                    x * scale[0] - self.draw_options.line_width + offset[0],
                    y * scale[1] - self.draw_options.line_width + offset[1],
                ),
                (
                    x * scale[0] + self.draw_options.line_width + offset[0],
                    y * scale[1] + self.draw_options.line_width + offset[1],
                ),
            ],
            fill=self.draw_options.draw_color,
        )
        return None

    def _calculate_scale(
        self,
    ):
        def_x_min, def_x_max, def_y_min, def_y_max = self.bounds
        intersect = self._intersect_draw_interval_image_size()
        return (
            intersect[0] / (def_x_max - def_x_min),
            intersect[1] / (def_y_max - def_y_min),
        )

    def _intersect_draw_interval_image_size(self):
        def_x_min, def_x_max, def_y_min, def_y_max = self.bounds
        image_x_min, image_x_max, image_y_min, image_y_max = self.image_bounds
        return (
            1 / ((image_x_max - image_x_min) / (def_x_max - def_x_min))
        ) * self.image.image_options.image_size[0], (
            1 / ((image_y_max - image_y_min) / (def_y_max - def_y_min))
        ) * self.image.image_options.image_size[
            1
        ]
