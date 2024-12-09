import torch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from color_gradient import GradientGenerator
from options_classes import DrawOptions, ImageOptions
from graphs_classes import ImplicitFunctionGraphFactory, ImplicitFunctionGraph
from make_animation import make_animation

size = (512, 512)
draw_bounds = [[-8, 8], [-8, 8]]


g1 = GradientGenerator().create_gradient([(32, 122, 220), (70, 220, 90)], 100)
g2 = GradientGenerator().create_gradient([(220, 70, 50), (130, 40, 215)], 100)
g3 = [(0, 0, 0)] * 100
make_animation(
    [0, 10],
    100,
    [
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: torch.tanh(
                    2 * torch.cos(t_x) ** 2 + 2 * torch.sin(t_y) ** 2
                )
                - torch.sin(p * t_y)
                + torch.sin((p / 10) * t_x)
                - 2 * torch.cos(t_x**2 + t_y**2),
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: torch.tanh(
                    2 * torch.cos(t_x) ** 2 + 2 * torch.sin(t_y) ** 2
                )
                + torch.sin(p * t_y)
                - torch.sin((p / 10) * t_x)
                - 2 * torch.cos(t_x**2 + t_y**2),
                "<",
                10e-5,
                draw_bounds,
            )
        ),
        ImplicitFunctionGraphFactory(
            lambda p: ImplicitFunctionGraph(
                lambda t_x, t_y: torch.maximum(
                    torch.tanh(2 * torch.cos(t_x) ** 2 + 2 * torch.sin(t_y) ** 2)
                    + torch.sin(p * t_y)
                    - torch.sin((p / 10) * t_x)
                    - 2 * torch.cos(t_x**2 + t_y**2),
                    torch.tanh(2 * torch.cos(t_x) ** 2 + 2 * torch.sin(t_y) ** 2)
                    - torch.sin(p * t_y)
                    + torch.sin((p / 10) * t_x)
                    - 2 * torch.cos(t_x**2 + t_y**2),
                ),
                "<",
                10e-5,
                draw_bounds,
            )
        ),
    ],
    [
        DrawOptions(1, (0, 0, 0)),
        DrawOptions(1, (0, 0, 0)),
        DrawOptions(1, (0, 0, 0)),
    ],
    ImageOptions(
        size=size,
        draw_bounds=draw_bounds,
        show_axes=False,
        background_color=(255, 255, 255),
    ),
    "results/animations/implicit_function_graph_variation_example.avi",
    resolution=size,
    color_gradients=[g1, g2, g3],
    device=torch.device("cpu"),
)
