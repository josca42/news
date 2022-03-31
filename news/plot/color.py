import matplotlib.pyplot as plt
from colorspacious import cspace_converter
import numpy as np
import bisect


def generate_color_values(values, color_theme, n_colors):
    color_list = generate_color_list(color_theme, n_colors)
    color_intervals = generate_intervals(values, n_colors)
    return [
        assign_color_group(
            colors=color_list, color_intervals=color_intervals, value=val
        )
        for val in values
    ]


def generate_color_list(color_theme, n_colors):
    """
    Generate list of rgb colors.

    color_theme: matplotlib color theme
    N: number of colors in color list i.e. level of granularity.
    """
    x = np.linspace(0, 1, n_colors)
    rgb = plt.get_cmap(color_theme)(x)[np.newaxis, :, :3]
    lab = cspace_converter("sRGB1", "sRGB255")(rgb)
    return lab.squeeze()


def generate_intervals(values, n_colors):
    """
    Generate list of numbers denoting the color intervals
    """
    start, middle, end = np.percentile(values, [2.5, 85, 99])

    # color_intervals = np.linspace(start, end, n_colors - 1)

    n_1 = int(n_colors * 0.85)
    n_2 = n_colors - n_1 - 1

    color_intervals = np.hstack(
        [np.linspace(start, middle, n_1), np.geomspace(middle, end, n_2)]
    )
    return color_intervals


def assign_color_group(colors, color_intervals, value):
    color_pos = bisect.bisect_right(color_intervals, value)
    return list(colors[color_pos])
