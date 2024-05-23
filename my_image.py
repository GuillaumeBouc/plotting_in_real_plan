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
