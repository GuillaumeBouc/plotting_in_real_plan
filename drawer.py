import numpy as np
from PIL import ImageDraw
from typing import Tuple, Union

from parametric_curve import ParametricCurve
from implicit_function_graph import ImplicitFunctionGraph
from draw_options import DrawOptions
from my_image import MyImage


class Drawer:
    def __init__(
        self,
        curve: Union[ParametricCurve, ImplicitFunctionGraph],
        draw_options: DrawOptions,
        image: MyImage,
        name: str,
    ) -> None:
        self.curve = curve
        self.draw_options = draw_options
        self.image = image
        self.name = name
        self.image_bounds = self._get_bounds(image.options.draw_bounds)
        self.curve_bounds = self._get_curve_bounds()

    def draw(self) -> None:
        if isinstance(self.curve, ParametricCurve):
            self._draw_parametric_curve()
        elif isinstance(self.curve, ImplicitFunctionGraph):
            if self._definition_interval_in_draw_interval():
                self._draw_implicit_function_graph()
            else:
                raise ValueError(
                    "The definition interval of the implicit function graph is not in the draw interval"
                )
        else:
            raise ValueError("Unsupported curve type")

    def _get_bounds(
        self, bounds: list[list[float]]
    ) -> Tuple[float, float, float, float]:
        return (bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])

    def _get_curve_bounds(self) -> Tuple[float, float, float, float]:
        if isinstance(self.curve, ParametricCurve):
            return self._get_bounds(self.curve.draw_interval_bounds)
        elif isinstance(self.curve, ImplicitFunctionGraph):
            return self._get_bounds(self.curve.interval_bounds)
        else:
            raise ValueError("Unsupported curve type")

    def _draw_parametric_curve(self) -> None:
        t_min, t_max = self.curve.interval_bounds
        x_func, y_func = self.curve.x_func, self.curve.y_func

        scale = self._calculate_scale()
        offset = self._calculate_offset(scale)
        print(f"parameter between {t_min} and {t_max}")

        for t in np.linspace(t_min, t_max, self.image.options.size[0]):
            x, y = x_func(t), y_func(t)
            self._draw_point(x, y, scale, offset)

    def _draw_implicit_function_graph(self) -> None:
        scale = self._calculate_scale()
        offset = self._calculate_offset(scale)
        intersect_size = self._intersect_draw_interval_image_size()

        x_range, y_range = self._get_draw_ranges()
        print(
            f"x between {x_range[0]} and {x_range[1]}, y between {y_range[0]} and {y_range[1]}"
        )

        for x in np.linspace(*x_range, round(intersect_size[0])):
            for y in np.linspace(*y_range, round(intersect_size[1])):
                if self.curve.equation(float(x), float(y)):
                    self._draw_point(x, y, scale, offset)

    def _definition_interval_in_draw_interval(self) -> bool:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return any(
            img_x_min <= bound <= img_x_max and img_y_min <= bound <= img_y_max
            for bound in [def_x_min, def_x_max, def_y_min, def_y_max]
        )

    def _draw_point(
        self,
        x: float,
        y: float,
        scale: Tuple[float, float],
        offset: Tuple[float, float],
    ) -> None:
        draw = self.image.draw
        line_width = self.draw_options.line_width
        draw.ellipse(
            [
                (
                    x * scale[0] - line_width + offset[0],
                    y * scale[1] - line_width + offset[1],
                ),
                (
                    x * scale[0] + line_width + offset[0],
                    y * scale[1] + line_width + offset[1],
                ),
            ],
            fill=self.draw_options.draw_color,
        )

    def _calculate_scale(self) -> Tuple[float, float]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        intersect_size = self._intersect_draw_interval_image_size()
        return (
            intersect_size[0] / (def_x_max - def_x_min),
            intersect_size[1] / (def_y_max - def_y_min),
        )

    def _calculate_offset(self, scale: Tuple[float, float]) -> Tuple[float, float]:
        img_x_min, _, img_y_min, _ = self.image_bounds
        return (-img_x_min * scale[0], -img_y_min * scale[1])

    def _intersect_draw_interval_image_size(self) -> Tuple[float, float]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return (
            (1 / ((img_x_max - img_x_min) / (def_x_max - def_x_min)))
            * self.image.options.size[0],
            (1 / ((img_y_max - img_y_min) / (def_y_max - def_y_min)))
            * self.image.options.size[1],
        )

    def _get_draw_ranges(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return (
            (max(def_x_min, img_x_min), min(def_x_max, img_x_max)),
            (max(def_y_min, img_y_min), min(def_y_max, img_y_max)),
        )
