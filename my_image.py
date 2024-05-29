from PIL import Image, ImageDraw

from image_options import ImageOptions


class MyImage:
    def __init__(self, image_options: ImageOptions) -> None:
        self.image_options = image_options
        self.image = Image.new(
            "RGB", self.image_options.image_size, self.image_options.background_color
        )
        self.draw = ImageDraw.Draw(self.image)
        self.name = self.image_options.image_name

        if self.image_options.has_axis:
            self._draw_frame()

    #  découpe en d'autres methodes et appelle les toutes ici
    def _draw_frame(self) -> None:
        # draw x and y axis with mesure of 1 and image_option.interval_bounds

        x_min, x_max = self.image_options.draw_interval_bounds[0]
        y_min, y_max = self.image_options.draw_interval_bounds[1]
        scale = (
            self.image_options.image_size[0] / (x_max - x_min),
            self.image_options.image_size[1] / (y_max - y_min),
        )
        offset = (-x_min * scale[0], -y_min * scale[1])

        # draw an background ligth-grey grid
        for i in range(int(x_min), int(x_max)):
            self.draw.line(
                [
                    (i * scale[0] + offset[0], 0),
                    (i * scale[0] + offset[0], self.image_options.image_size[1]),
                ],
                fill=(180, 180, 180),
                width=2,
            )
        for i in range(int(y_min), int(y_max)):
            self.draw.line(
                [
                    (0, i * scale[1] + offset[1]),
                    (self.image_options.image_size[0], i * scale[1] + offset[1]),
                ],
                fill=(180, 180, 180),
                width=2,
            )

        # draw x and y axis
        self.draw.line(
            [
                (0, offset[1]),
                (self.image_options.image_size[0], offset[1]),
            ],
            fill=self.image_options.axis_color,
            width=self.image_options.axis_width,
        )
        self.draw.line(
            [
                (offset[0], 0),
                (offset[0], self.image_options.image_size[1]),
            ],
            fill=self.image_options.axis_color,
            width=self.image_options.axis_width,
        )
        # draw ticks
        for i in range(int(x_min), int(x_max)):
            self.draw.line(
                [
                    (i * scale[0] + offset[0], offset[1] - 15),
                    (i * scale[0] + offset[0], offset[1] + 15),
                ],
                fill=self.image_options.axis_color,
                width=self.image_options.axis_width,
            )
        for i in range(int(y_min), int(y_max)):
            self.draw.line(
                [
                    (offset[0] - 15, i * scale[1] + offset[1]),
                    (offset[0] + 15, i * scale[1] + offset[1]),
                ],
                fill=self.image_options.axis_color,
                width=self.image_options.axis_width,
            )
