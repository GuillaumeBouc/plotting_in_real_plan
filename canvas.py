from typing import Tuple
import torch

from options_classes import ImageOptions


class Canvas:
    def __init__(self, options: ImageOptions) -> None:
        self.options = options
        self.image = torch.zeros(
            (
                self.options.size[1],
                self.options.size[0],
                3,
            ),
            dtype=torch.uint8,
        )

        background_color = torch.tensor(
            self.options.background_color, dtype=torch.uint8
        )
        self.image[:, :, 0] = background_color[0]
        self.image[:, :, 1] = background_color[1]
        self.image[:, :, 2] = background_color[2]
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
            x = int(i * scale_x + offset_x)
            self.image[:, x, :] = torch.tensor(
                self.options.grid_color, dtype=torch.uint8
            )

        for i in range(int(y_min), int(y_max) + 1):
            y = int(i * scale_y + offset_y)
            self.image[y, :, :] = torch.tensor(
                self.options.grid_color, dtype=torch.uint8
            )

    def _draw_axes(self) -> None:
        scale_x, scale_y = self._calculate_scale()
        offset_x, offset_y = self._calculate_offset(scale_x, scale_y)

        offset_x = int(offset_x)
        offset_y = int(offset_y)

        # Horizontal axis
        self.image[offset_y, :, :] = torch.tensor(
            self.options.axis_color, dtype=torch.uint8
        )
        # Vertical axis
        self.image[:, offset_x, :] = torch.tensor(
            self.options.axis_color, dtype=torch.uint8
        )

    def _draw_ticks(self) -> None:
        x_min, x_max = self.options.draw_bounds[0]
        y_min, y_max = self.options.draw_bounds[1]
        scale_x, scale_y = self._calculate_scale()
        offset_x, offset_y = self._calculate_offset(scale_x, scale_y)
        tick_length = self.options.tick_length

        for i in range(int(x_min), int(x_max) + 1):
            x = int(i * scale_x + offset_x)
            self.image[
                int(offset_y - tick_length) : int(offset_y + tick_length), x, :
            ] = torch.tensor(self.options.axis_color, dtype=torch.uint8)

        for i in range(int(y_min), int(y_max) + 1):
            y = int(i * scale_y + offset_y)
            self.image[
                y, int(offset_x - tick_length) : int(offset_x + tick_length), :
            ] = torch.tensor(self.options.axis_color, dtype=torch.uint8)

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

    def save(self, path: str) -> None:
        from PIL import Image

        pil_image = Image.fromarray(self.image.numpy())
        pil_image.save(path)
