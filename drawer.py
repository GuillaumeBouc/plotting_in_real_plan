from typing import Tuple, Union
import torch

from graphs_classes import ParametricCurve, ImplicitFunctionGraph
from options_classes import DrawOptions
from canvas import Canvas


class Drawer:
    def __init__(
        self,
        curve: Union[ParametricCurve, ImplicitFunctionGraph],
        draw_options: DrawOptions,
        image: Canvas,
        name: str,
    ) -> None:
        self.curve = curve
        self.draw_options = draw_options
        self.image = image
        self.name = name
        self.image_bounds = self._get_bounds(image.options.draw_bounds)
        self.curve_bounds = self._get_curve_bounds()

    def draw(
        self,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        if isinstance(self.curve, ParametricCurve):
            self._draw_parametric_curve()
        elif isinstance(self.curve, ImplicitFunctionGraph):
            if self._definition_interval_in_draw_interval():
                self._draw_implicit_function_graph(device)
            else:
                raise ValueError(
                    "The definition interval of the implicit function graph is not in the draw interval"
                )
        else:
            raise ValueError("Unsupported curve type")

    def _get_bounds(self, bounds: list[list[float]]) -> Tuple[float]:
        return (bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])

    def _get_curve_bounds(self) -> Tuple[float]:
        if isinstance(self.curve, ParametricCurve):
            return self._get_bounds(self.curve.draw_interval_bounds)
        elif isinstance(self.curve, ImplicitFunctionGraph):
            return self._get_bounds(self.curve.interval_bounds)
        else:
            raise ValueError("Unsupported curve type")

    def _draw_parametric_curve(
        self, device: torch.device = torch.device("cpu")
    ) -> None:
        t_min, t_max = self.curve.interval_bounds
        x_func, y_func = self.curve.x_func, self.curve.y_func

        scale = self._calculate_scale()
        offset = self._calculate_offset(scale)
        print(f"parameter between {t_min} and {t_max}")

        # Create a tensor of equally spaced points
        t = torch.linspace(t_min, t_max, self.curve.precision, device=device)

        # Calculate x and y coordinates using the parametric functions
        x = x_func(t)
        y = y_func(t)

        # Calculate pixel coordinates
        pixel_x = ((x * scale[0]) + offset[0]).long()
        pixel_y = ((y * scale[1]) + offset[1]).long()

        # Clamp pixel coordinates to image bounds
        pixel_x = pixel_x.clamp(0, self.image.options.size[0] - 1)
        pixel_y = pixel_y.clamp(0, self.image.options.size[1] - 1)

        # Draw points on the image
        self.image.image[pixel_y, pixel_x] = torch.tensor(
            self.draw_options.draw_color, dtype=torch.uint8
        )

    def _draw_implicit_function_graph(self, device: torch.device) -> None:
        scale = self._calculate_scale()
        offset = self._calculate_offset(scale)
        intersect_size = self._intersect_draw_interval_image_size()

        x_range, y_range = self._get_draw_ranges()
        print(
            f"x between {x_range[0]} and {x_range[1]}, y between {y_range[0]} and {y_range[1]}"
        )
        t_x, t_y = (
            torch.linspace(*x_range, round(intersect_size[0]), device=device),
            torch.linspace(*y_range, round(intersect_size[1]), device=device),
        )
        x_grid, y_grid = torch.meshgrid(t_x, t_y, indexing="ij")
        mask = self.curve.equation(x_grid, y_grid)

        pixel_x = ((x_grid[mask] * scale[0]) + offset[0]).long()
        pixel_y = ((y_grid[mask] * scale[1]) + offset[1]).long()

        pixel_x = pixel_x.clamp(0, self.image.options.size[0] - 1)
        pixel_y = pixel_y.clamp(0, self.image.options.size[1] - 1)

        self.image.image[pixel_y, pixel_x] = torch.tensor(
            self.draw_options.draw_color, dtype=torch.uint8
        )

    def _definition_interval_in_draw_interval(self) -> bool:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return any(
            img_x_min <= bound <= img_x_max and img_y_min <= bound <= img_y_max
            for bound in [def_x_min, def_x_max, def_y_min, def_y_max]
        )

    def _calculate_scale(self) -> Tuple[float]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        intersect_size = self._intersect_draw_interval_image_size()
        return (
            intersect_size[0] / (def_x_max - def_x_min),
            intersect_size[1] / (def_y_max - def_y_min),
        )

    def _calculate_offset(self, scale: Tuple[float]) -> Tuple[float]:
        img_x_min, _, img_y_min, _ = self.image_bounds
        return (-img_x_min * scale[0], -img_y_min * scale[1])

    def _intersect_draw_interval_image_size(self) -> Tuple[float]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return (
            (1 / ((img_x_max - img_x_min) / (def_x_max - def_x_min)))
            * self.image.options.size[0],
            (1 / ((img_y_max - img_y_min) / (def_y_max - def_y_min)))
            * self.image.options.size[1],
        )

    def _get_draw_ranges(self) -> Tuple[Tuple[float], Tuple[float]]:
        def_x_min, def_x_max, def_y_min, def_y_max = self.curve_bounds
        img_x_min, img_x_max, img_y_min, img_y_max = self.image_bounds
        return (
            (max(def_x_min, img_x_min), min(def_x_max, img_x_max)),
            (max(def_y_min, img_y_min), min(def_y_max, img_y_max)),
        )
