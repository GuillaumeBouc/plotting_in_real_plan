from typing import List, Union, Tuple

import numpy as np
import cv2
import torch

from graphs_classes import (
    ImplicitFunctionGraphFactory,
    PolarCurveFactory,
    ParametricCurveFactory,
    FunctionCurveFactory,
)
from options_classes import DrawOptions, ImageOptions
from main import main


def make_animation(
    bounds: List[float],
    num_steps: int,
    factories: List[
        Union[
            ImplicitFunctionGraphFactory,
            PolarCurveFactory,
            ParametricCurveFactory,
            FunctionCurveFactory,
        ]
    ],
    draw_options: List[DrawOptions],
    image_options: ImageOptions,
    output_file_name: str,
    resolution: Tuple[int] = None,
    FPS: int = 60,
    color_gradients: List[List[Tuple[int, int, int]]] = None,
    device: torch.device = torch.device("cpu"),
) -> None:

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(
        output_file_name, fourcc, FPS, resolution or image_options.size
    )

    param_values = np.linspace(bounds[0], bounds[1], num_steps)

    if color_gradients is not None:
        for color_gradient in color_gradients:
            assert len(color_gradient) == num_steps

    for param_index, param in enumerate(param_values):

        image_options.name = str(param_index)

        curves_per_name = {}
        draw_options_per_name = {}

        for func_index, (factory, draw_option) in enumerate(
            zip(factories, draw_options)
        ):
            curves_per_name[f"{param_index}_{func_index}"] = factory(param)

            if color_gradient is not None:
                draw_option.draw_color = color_gradients[func_index][param_index]

            draw_options_per_name[f"{param_index}_{func_index}"] = draw_option

        img = np.array(
            main(
                curves_per_name,
                image_options,
                draw_options_per_name,
                default_draw_options=DrawOptions(1, (0, 0, 0)),
                device=device,
            )
        )

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if img is None:
            print(f"Warning : image could not be read.")
            continue
        if img.size != resolution:
            img = cv2.resize(img, resolution)
        out.write(img)
        print(f"Add image n°{image_options.name} to the animation\n")

    out.release()
