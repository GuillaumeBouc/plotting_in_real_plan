from typing import List, Tuple, Dict, Type
from .color_spaces import ColorSpace, RGBSpace, HSLSpace, HSVSpace
from .easing import Easing, EasingFunction
from .color_utils import ColorUtils


class GradientGenerator:
    def __init__(self):
        self.color_spaces: Dict[str, Type[ColorSpace]] = {
            "RGB": RGBSpace(),
            "HSL": HSLSpace(),
            "HSV": HSVSpace(),
        }

    def create_gradient(
        self,
        colors: List[Tuple[int, int, int]],
        steps: int,
        colorspace: str = "HSL",
        easing: EasingFunction = Easing.linear,
        gamma: float = 1.0,
    ) -> List[Tuple[int, int, int]]:
        """
        Create a gradient between multiple colors with customizable parameters.

        Args:
            colors: List of RGB tuples [(r,g,b), ...] with values 0-255
            steps: Number of colors in the output gradient
            colorspace: Color space to perform interpolation in ("RGB", "HSL", "HSV")
            easing: Easing function to control the progression
            gamma: Gamma correction value (1.0 means no correction)

        Returns:
            List of RGB tuples representing the gradient
        """
        if len(colors) < 2:
            raise ValueError("Color list must contain at least two colors")
        if steps < 2:
            raise ValueError("Steps must be at least 2")

        color_space = self.color_spaces.get(colorspace)
        if not color_space:
            raise ValueError(f"Unsupported color space: {colorspace}")

        # Convert colors to 0-1 range and chosen color space
        normalized_colors = [ColorUtils.normalize_rgb(c) for c in colors]
        converted_colors = [color_space.convert_to(c) for c in normalized_colors]

        # Apply gamma correction if needed
        if gamma != 1.0:
            converted_colors = [
                ColorUtils.apply_gamma(c, gamma) for c in converted_colors
            ]

        gradient = []
        for i in range(steps):
            # Apply easing to the progress
            progress = easing(i / (steps - 1))
            idx = progress * (len(colors) - 1)

            # Find the two colors to interpolate between
            idx1 = int(idx)
            idx2 = min(idx1 + 1, len(colors) - 1)
            fraction = idx - idx1

            # Interpolate between colors
            c1 = converted_colors[idx1]
            c2 = converted_colors[idx2]
            interpolated = self._interpolate_colors(
                c1, c2, fraction, color_space.hue_positions
            )

            # Remove gamma correction if needed
            if gamma != 1.0:
                interpolated = ColorUtils.remove_gamma(interpolated, gamma)

            # Convert back to RGB and 0-255 range
            rgb_color = color_space.convert_from(interpolated)
            gradient.append(ColorUtils.denormalize_rgb(rgb_color))

        return gradient

    def _interpolate_colors(
        self,
        color1: Tuple[float, ...],
        color2: Tuple[float, ...],
        fraction: float,
        is_hue: Tuple[bool, bool, bool],
    ) -> Tuple[float, ...]:
        """Interpolate between two colors, handling hue specially"""
        result = []
        for i, (c1, c2) in enumerate(zip(color1, color2)):
            if is_hue[i]:
                result.append(ColorUtils.interpolate_hue(c1, c2, fraction))
            else:
                result.append(c1 + fraction * (c2 - c1))
        return tuple(result)
