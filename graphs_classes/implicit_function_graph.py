from dataclasses import dataclass
from typing import Callable, List
from dataclasses import dataclass
import torch


@dataclass
class ImplicitFunctionGraph:
    term: Callable[
        [torch.Tensor, torch.Tensor], torch.Tensor
    ]  # the left term of an equation whose right term is 0
    sign: str  # must be in ["=", "<", ">"]
    tolerance: float
    interval_bounds: List[List[float]]

    def __post_init__(self) -> None:
        if self.sign not in ["=", "<", ">"]:
            raise ValueError("Invalid sign type")

    @property
    def equation(self) -> Callable[[torch.Tensor], torch.Tensor]:
        if self.sign == "=":
            return lambda t_x, t_y: torch.where(
                torch.abs(self.term(t_x, t_y))
                < torch.full_like(t_x, fill_value=self.tolerance),
                True,
                False,
            )
        elif self.sign == "<":
            return lambda t_x, t_y: torch.where(
                self.term(t_x, t_y) < torch.full_like(t_x, fill_value=self.tolerance),
                True,
                False,
            )
        elif self.sign == ">":
            return lambda t_x, t_y: torch.where(
                self.term(t_x, t_y) > torch.full_like(t_x, fill_value=self.tolerance),
                True,
                False,
            )
