from typing import Tuple


class ColorUtils:
    @staticmethod
    def normalize_rgb(color: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB values from 0-255 to 0-1"""
        return tuple(c / 255 for c in color)

    @staticmethod
    def denormalize_rgb(color: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Convert RGB values from 0-1 to 0-255"""
        return tuple(min(255, max(0, int(c * 255))) for c in color)

    @staticmethod
    def interpolate_hue(h1: float, h2: float, fraction: float) -> float:
        """Interpolate between two hue values, taking the shortest path"""
        diff = h2 - h1
        if abs(diff) > 0.5:
            if h1 > h2:
                h2 += 1.0
            else:
                h1 += 1.0
        return (h1 + fraction * (h2 - h1)) % 1.0

    @staticmethod
    def apply_gamma(color: Tuple[float, ...], gamma: float) -> Tuple[float, ...]:
        """Apply gamma correction to a color tuple"""
        if gamma == 1.0:
            return color
        return tuple(pow(c, gamma) for c in color)

    @staticmethod
    def remove_gamma(color: Tuple[float, ...], gamma: float) -> Tuple[float, ...]:
        """Remove gamma correction from a color tuple"""
        if gamma == 1.0:
            return color
        return tuple(pow(c, 1 / gamma) for c in color)
