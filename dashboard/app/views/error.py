# flake8: noqa E501

from dash import dcc
from dash import html

from dashboard.app.components.wrappers import main_wrapper


def layout(sidebar_context):
    return main_wrapper(
        html.Div(
            [
                html.Div("404", className="error mx-auto", **{"data-text": "404"}),
                html.P("Page Not Found", className="lead text-gray-800 mb-5"),
                html.P(
                    "It looks like you found a glitch in the matrix...",
                    className="text-gray-500 mb-0",
                ),
                dcc.Link("← Back to Dashboard", href="/"),
            ],
            className="text-center",
        ),
        sidebar_context,
    )
