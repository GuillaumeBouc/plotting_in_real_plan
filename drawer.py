import numpy as np
from PIL import Image, ImageDraw

from parametric_curve import ParametricCurve
from draw_option import DrawOption
from image_option import ImageOption


class Drawer:
    def __init__(self, parametric_curve: ParametricCurve) -> None:
        self.parametric_curve = parametric_curve

    def draw(self, draw_option: DrawOption, image_option: ImageOption) -> Image:

        image = Image.new("RGB", image_option.image_size, image_option.background_color)
        draw = ImageDraw.Draw(image)
        self._draw_curve(draw, draw_option, image_option)
        return image.transpose(Image.FLIP_TOP_BOTTOM)

    def _draw_curve(
        self, draw: ImageDraw, draw_option: DrawOption, image_option: ImageOption
    ) -> None:
        t_min, t_max = self.parametric_curve.interval_bounds
        x_func, y_func = self.parametric_curve.x_func, self.parametric_curve.y_func
        x_min, x_max = image_option.draw_interval_bounds[0]
        y_min, y_max = image_option.draw_interval_bounds[1]
        scale = (
            image_option.image_size[0] / (x_max - x_min),
            image_option.image_size[1] / (y_max - y_min),
        )
        offset = (-x_min * scale[0], -y_min * scale[1])

        for t in np.linspace(t_min, t_max, image_option.image_size[0]):
            x = x_func(t)
            y = y_func(t)

            draw.ellipse(
                [
                    (
                        x * scale[0] - draw_option.draw_width + offset[0],
                        y * scale[1] - draw_option.draw_width + offset[1],
                    ),
                    (
                        x * scale[0] + draw_option.draw_width + offset[0],
                        y * scale[1] + draw_option.draw_width + offset[1],
                    ),
                ],
                fill=draw_option.draw_color,
            )
        return None


if __name__ == "__main__":
    parametric_curve = ParametricCurve(
        interval_bounds=[0, 6 * np.pi],
        x_func=lambda t: 2 * np.cos(t) + 5 * np.cos(2 * t / 3),
        y_func=lambda t: 2 * np.sin(t) - 5 * np.sin(2 * t / 3),
    )

    # parametric_curve = ParametricCurve(
    #     interval_bounds=[-10, 10],
    #     x_func=lambda t: t,
    #     y_func=lambda t: t**3 + t**2 + t + 1,
    # )
    draw_option = DrawOption(draw_width=10, draw_color=(255, 0, 0))
    image_option = ImageOption(
        image_size=(2000, 2000),
        draw_interval_bounds=[[-5, 5], [-5, 5]],
        background_color=(255, 255, 255),
    )

    drawer = Drawer(parametric_curve)
    image = drawer.draw(draw_option, image_option)
    image.show()
    image.save("parametric_curve.png")
