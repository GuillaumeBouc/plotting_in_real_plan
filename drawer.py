import numpy as np
from PIL import Image, ImageDraw

from parametric_curve import ParametricCurve
from draw_options import DrawOptions
from image_options import ImageOptions
from my_image import MyImage


class Drawer:
    def __init__(
        self,
        parametric_curve: ParametricCurve,
        draw_options: DrawOptions,
        image: MyImage,
    ) -> None:
        self.parametric_curve = parametric_curve
        self.draw_options = draw_options
        self.image = image

    def draw(self) -> None:

        self._draw_curve(self.image.draw)

    def _draw_curve(self, draw: ImageDraw) -> None:

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
