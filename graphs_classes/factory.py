from typing import Callable
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from graphs_classes import (
    ParametricCurve,
    ImplicitFunctionGraph,
    FunctionCurve,
    PolarCurve,
)


class FunctionCurveFactory:
    def __init__(self, factory: Callable[[float], FunctionCurve]) -> None:
        self.factory = factory

    def __call__(self, param: float) -> ParametricCurve:
        return self.factory(param).to_parametric()


class PolarCurveFactory:
    def __init__(self, factory: Callable[[float], PolarCurve]) -> None:
        self.factory = factory

    def __call__(self, param: float) -> ParametricCurve:
        return self.factory(param).to_parametric()


class ParametricCurveFactory:
    def __init__(self, factory: Callable[[float], ParametricCurve]) -> None:
        self.factory = factory

    def __call__(self, param: float) -> ParametricCurve:
        return self.factory(param)


class ImplicitFunctionGraphFactory:
    def __init__(self, factory: Callable[[float], ImplicitFunctionGraph]) -> None:
        self.factory = factory

    def __call__(self, param: float) -> ImplicitFunctionGraph:
        return self.factory(param)
