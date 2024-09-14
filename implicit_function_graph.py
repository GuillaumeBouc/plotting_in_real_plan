from dataclasses import dataclass
from typing import Callable, List


@dataclass
class ImplicitFunctionGraph:
    left_term: Callable[[float, float], float]
    right_term: Callable[[float, float], float]
    sign: str  # must be in ["=", "<", ">"]
    tolerance: float
    interval_bounds: List[List[float]]

    def __post_init__(self) -> None:
        if self.sign not in ["=", "<", ">"]:
            raise ValueError("Invalid sign type")

    @property
    def equation(self) -> Callable[[float, float], float]:
        if self.sign == "=":
            return (
                lambda x, y: abs(
                    float(self.left_term(x, y)) - float(self.right_term(x, y))
                )
                < self.tolerance
            )
        elif self.sign == "<":
            return (
                lambda x, y: self.left_term(x, y) - self.right_term(x, y)
                < self.tolerance
            )
        elif self.sign == ">":
            return (
                lambda x, y: self.left_term(x, y) - self.right_term(x, y)
                > -self.tolerance
            )
