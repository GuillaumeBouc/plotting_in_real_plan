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
        x_min, x_max = image.image_options.draw_interval_bounds[0]
        y_min, y_max = image.image_options.draw_interval_bounds[1]
        scale = (
            image.image_options.image_size[0] / (x_max - x_min),
            image.image_options.image_size[1] / (y_max - y_min),
        )
        offset = (-x_min * scale[0], -y_min * scale[1])

        for t in np.linspace(t_min, t_max, image.image_options.image_size[0]):
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


if __name__ == "__main__":

    image_options = ImageOptions(
        image_size=(4000, 4000),
        draw_interval_bounds=[[-15, 15], [-15, 15]],
        background_color=(255, 255, 255),
    )

    image = MyImage(image_options)

    draw_options_and_parametric_curve_per_name = {
        "star": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                x_func=lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3) + 7.5,
                y_func=lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3) + 7.5,
            ),
            DrawOptions(draw_color=(72, 190, 240), draw_width=20),
        ],
        "circle": [
            ParametricCurve(
                interval_bounds=[0, 2 * np.pi],
                x_func=lambda t: np.cos(t),
                y_func=lambda t: np.sin(t),
            ),
            DrawOptions(draw_color=(240, 232, 72), draw_width=20),
        ],
        "circle_2": [
            ParametricCurve(
                interval_bounds=[0, 2 * np.pi],
                x_func=lambda t: 3 * np.cos(t),
                y_func=lambda t: 3 * np.sin(t),
            ),
            DrawOptions(draw_color=(240, 232, 72), draw_width=20),
        ],
        "heart": [
            ParametricCurve(
                interval_bounds=[0, 6 * np.pi],
                x_func=lambda t: (8 * np.cos(t) - 6 * np.cos(8 * t / 3)) / 2 - 7.5,
                y_func=lambda t: (8 * np.sin(t) - 6 * np.sin(8 * t / 3)) / 2 - 7.5,
            ),
            DrawOptions(draw_color=(240, 72, 100), draw_width=20),
        ],
        "some_curve": [
            ParametricCurve(
                interval_bounds=[-15, 0],
                x_func=lambda t: t,
                y_func=lambda t: t + 15 + 2 * np.sin(3 * t) + 2 * np.cos(2 * t),
            ),
            DrawOptions(draw_color=(125, 240, 75), draw_width=20),
        ],
        "spiral": [
            ParametricCurve(
                interval_bounds=[0, 4 * np.pi],
                x_func=lambda t: 0.5 * t * np.cos(t) + 8 + np.cos(t),
                y_func=lambda t: 0.5 * t * np.sin(t) - 8 + np.cos(t),
            ),
            DrawOptions(draw_color=(240, 180, 30), draw_width=20),
        ],
    }

    drawers = [
        Drawer(parametric, draw_option, image)
        for parametric, draw_option in draw_options_and_parametric_curve_per_name.values()
    ]

    for drawer in drawers:
        drawer.draw()

    image.image.transpose(Image.FLIP_TOP_BOTTOM).save(f"image/{image.name}.png")
