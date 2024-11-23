from PIL import Image, ImageDraw
from options_classes.image_options import ImageOptions
from typing import Tuple


class Canvas:
    def __init__(self, options: ImageOptions) -> None:
        self.options = options
        self.image = Image.new("RGB", self.options.size, self.options.background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.name = self.options.name

        if self.options.show_axes:
            self._draw_frame()

    def _draw_frame(self) -> None:
        self._draw_grid()
        self._draw_axes()
        self._draw_ticks()

    def _draw_grid(self) -> None:
        x_min, x_max = self.options.draw_bounds[0]
        y_min, y_max = self.options.draw_bounds[1]
        scale_x, scale_y = self._calculate_scale()
        offset_x, offset_y = self._calculate_offset(scale_x, scale_y)

        for i in range(int(x_min), int(x_max) + 1):
            x = i * scale_x + offset_x
            self.draw.line(
                [(x, 0), (x, self.options.size[1])],
                fill=self.options.grid_color,
                width=self.options.grid_width,
            )

        for i in range(int(y_min), int(y_max) + 1):
            y = i * scale_y + offset_y
            self.draw.line(
                [(0, y), (self.options.size[0], y)],
                fill=self.options.grid_color,
                width=self.options.grid_width,
            )

    def _draw_axes(self) -> None:
        scale_x, scale_y = self._calculate_scale()
        offset_x, offset_y = self._calculate_offset(scale_x, scale_y)

        self.draw.line(
            [(0, offset_y), (self.options.size[0], offset_y)],
            fill=self.options.axis_color,
            width=self.options.axis_width,
        )
        self.draw.line(
            [(offset_x, 0), (offset_x, self.options.size[1])],
            fill=self.options.axis_color,
            width=self.options.axis_width,
        )

    def _draw_ticks(self) -> None:
        x_min, x_max = self.options.draw_bounds[0]
        y_min, y_max = self.options.draw_bounds[1]
        scale_x, scale_y = self._calculate_scale()
        offset_x, offset_y = self._calculate_offset(scale_x, scale_y)
        tick_length = self.options.tick_length

        for i in range(int(x_min), int(x_max) + 1):
            x = i * scale_x + offset_x
            self.draw.line(
                [(x, offset_y - tick_length), (x, offset_y + tick_length)],
                fill=self.options.axis_color,
                width=self.options.axis_width,
            )

        for i in range(int(y_min), int(y_max) + 1):
            y = i * scale_y + offset_y
            self.draw.line(
                [(offset_x - tick_length, y), (offset_x + tick_length, y)],
                fill=self.options.axis_color,
                width=self.options.axis_width,
            )

    def _calculate_scale(self) -> Tuple[float, float]:
        x_min, x_max = self.options.draw_bounds[0]
        y_min, y_max = self.options.draw_bounds[1]
        return (
            self.options.size[0] / (x_max - x_min),
            self.options.size[1] / (y_max - y_min),
        )

    def _calculate_offset(self, scale_x: float, scale_y: float) -> Tuple[float, float]:
        x_min, _ = self.options.draw_bounds[0]
        y_min, _ = self.options.draw_bounds[1]
        return (-x_min * scale_x, -y_min * scale_y)
