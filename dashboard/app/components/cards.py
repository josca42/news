# flake8: noqa E501
from dash import dcc
from dash import html
from dash.dcc.Tab import Tab
from dash.dcc.Tabs import Tabs


def card(title, icon, value=None, color="primary", id=None):
    return html.Div(
        html.Div(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                title,
                                className=f"text-xs fw-bold text-{color} text-uppercase mb-1",
                            ),
                            html.Div(
                                value,
                                id=id if id else "",
                                className="h5 mb-0 fw-bold text-gray-800",
                            ),
                        ],
                        className="col me-2",
                    ),
                    html.Div(html.I(className=icon), className="col-auto"),
                ],
                className="row no-gutters align-items-center",
            ),
            className="card-body",
        ),
        className=f"card border-left-{color} shadow h-100 py-2",
    )


def grid_card(title, element, dropdown_options=None):
    return html.Div(
        [
            html.Div(
                [
                    html.H6(
                        title,
                        className="m-0 fw-bold text-primary",
                    ),
                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"
                                ),
                                className="dropdown-toggle",
                                role="button",
                                id="dropdownMenuLink",
                                **{
                                    "data-bs-toggle": "dropdown",
                                    "aria-haspopup": "true",
                                    "aria-expanded": "false",
                                },
                            ),
                            html.Div(
                                dropdown_options,
                                className="dropdown-menu dropdown-menu-right shadow animated--fade-in",
                                **{"aria-labelledby": "dropdownMenuLink"},
                            ),
                        ],
                        className="dropdown no-arrow",
                    )
                    if dropdown_options
                    else None,
                ],
                className="card-header py-3 d-flex flex-row align-items-center justify-content-between",
            ),
            dcc.Loading(
                html.Div(element, className="card-body h-100"),
                parent_className="h-100",
                color="var(--bs-primary)",
            ),
        ],
        className="card shadow mb-4 h-100",
    )


def tab_card(element, id, elements, value=None):
    return html.Div(
        [
            dcc.Tabs(
                [
                    dcc.Tab(
                        label=element["label"],
                        value=element["value"],
                        className="tab-card",
                        selected_className="tab-card-enabled",
                        disabled_className="tab-card-disabled",
                    )
                    for element in elements
                ],
                id=id,
                value=value,
            ),
            dcc.Loading(
                html.Div(element, className="card-body h-100", id=f"{id}Body"),
                parent_className="h-100",
                color="var(--bs-primary)",
            ),
        ],
        className="card shadow mb-4 h-100",
        style={"overflow": "hidden"},
    )
