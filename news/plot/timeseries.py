from news.plot.layout import BASE_LAYOUT, DEFAULT_PLOTLY_COLORS
from copy import copy
import plotly.graph_objects as go


def base(df, var, val2name: dict = {}):
    layout = copy(BASE_LAYOUT)

    fig = go.Figure(layout=layout)
    for i, val in enumerate(df[var].unique()):
        df_ts = df[df[var] == val]
        fig.add_trace(
            go.Scatter(
                x=df_ts.index,
                y=df_ts["count"],
                line=go.scatter.Line(color=DEFAULT_PLOTLY_COLORS[i], width=1.5),
                name=val2name[val] if val2name else val,
                hovertemplate="%{x}, %{y}",
                showlegend=False,
            )
        )
    return fig
