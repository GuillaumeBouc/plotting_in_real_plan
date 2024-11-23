from colorsys import rgb_to_hls, hls_to_rgb, rgb_to_hsv, hsv_to_rgb
from typing import Tuple, Protocol, runtime_checkable
from abc import ABC, abstractmethod


@runtime_checkable
class ColorSpace(Protocol):
    """Protocol defining color space conversion methods"""

    def convert_to(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]: ...

    def convert_from(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]: ...

    @property
    def hue_positions(self) -> Tuple[bool, bool, bool]:
        """Returns a tuple indicating which components are hue values"""
        ...


class RGBSpace:
    def convert_to(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return color

    def convert_from(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return color

    @property
    def hue_positions(self) -> Tuple[bool, bool, bool]:
        return (False, False, False)


class HSLSpace:
    def convert_to(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return rgb_to_hls(*color)

    def convert_from(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return hls_to_rgb(*color)

    @property
    def hue_positions(self) -> Tuple[bool, bool, bool]:
        return (True, False, False)


class HSVSpace:
    def convert_to(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return rgb_to_hsv(*color)

    def convert_from(
        self, color: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        return hsv_to_rgb(*color)

    @property
    def hue_positions(self) -> Tuple[bool, bool, bool]:
        return (True, False, False)
