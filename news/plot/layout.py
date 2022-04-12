BASE_LAYOUT = {
    "plot_bgcolor": "white",
    "font": {
        "size": 16,
        "family": "Kanit ExtraLight",
    },
    "legend": {
        "x": 0,
        "y": -0.1,
        "orientation": "h",
    },
    "xaxis": {
        "linecolor": "#1a1a39",
        "ticks": "inside",
        "tickangle": 30,
        "tickfont": {
            "size": 14,
        },
        "showgrid": False,
    },
    "yaxis": {
        "domain": [0.1, 1],
        "zeroline": False,
        "linecolor": "#1a1a39",
        "showtickprefix": "last",
        "ticks": "inside",
        "tickfont": {
            "size": 14,
        },
        "showgrid": False,
    },
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
}

DEFAULT_PLOTLY_COLORS = [
    "#1f77b4",  # muted blue
    "#ff7f0e",  # safety orange
    "#2ca02c",  # cooked asparagus green
    "#d62728",  # brick red
    "#9467bd",  # muted purple
    "#8c564b",  # chestnut brown
    "#e377c2",  # raspberry yogurt pink
    "#7f7f7f",  # middle gray
    "#bcbd22",  # curry yellow-green
    "#17becf",  # blue-teal
]
