# flake8: noqa E501
from time import sleep

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_deck
import pydeck as pdk
from news.db import crud
from news.plot.map import country_counts

from dashboard.app.app import app
from dashboard.app.components.cards import card, grid_card, tab_card
from dashboard.app.components.wrappers import main_wrapper
from datetime import datetime, timedelta
from news import config

GRAPH_LAYOUT = {"margin": {"t": 10, "l": 20, "r": 20, "b": 20}}


def layout(sidebar_context):

    graph_row1 = html.Div(
        [
            html.Div(
                grid_card(
                    "Event map",
                    dash_deck.DeckGL(
                        id="event-map",
                        mapboxKey=config["MAPBOX_API_KEY"],
                        # enableEvents=True,
                        # className="h-100",
                        # style={"minHeight": "100px"},
                        # responsive=True,
                    ),
                    dropdown_options=[
                        html.Div("Settings", className="dropdown-header"),
                        html.A(
                            "Download data",
                            id="download-data",
                            className="dropdown-item",
                        ),
                        html.A(
                            "change something",
                            id="change-something",
                            className="dropdown-item",
                        ),
                    ],
                ),
                className="col-12 col-md-12 pt-2 pb-4",
            ),
        ],
        className="row flex-grow-1",
    )

    # graph_row2 = html.Div(
    #     [
    #         html.Div(
    #             grid_card(
    #                 "Graph",
    #                 dcc.Graph(
    #                     id="graph2",
    #                     figure={"layout": GRAPH_LAYOUT, "data": []},
    #                     className="h-100",
    #                     style={"minHeight": "100px"},
    #                     responsive=True,
    #                 ),
    #             ),
    #             className="col-12 col-md-6 pt-2 pb-4",
    #         ),
    #         html.Div(
    #             tab_card(
    #                 None,
    #                 id="tab2",
    #                 elements=[
    #                     {"label": "Option 1", "value": "0"},
    #                     {"label": "Option 2", "value": "1"},
    #                     {"label": "Option 3", "value": "2"},
    #                 ],
    #                 value="0",
    #             ),
    #             className="col-12 col-md-6 pt-2 pb-4",
    #         ),
    #     ],
    #     className="row flex-grow-1",
    # )

    return main_wrapper(
        [graph_row1],
        sidebar_context,
    )


@app.callback(
    [Output("event-map", "data"), Output("event-map", "tooltip")],
    [Input("urlNoRefresh", "href")],
)
def update_event_map(_):
    start_date = datetime.now()
    end_date = start_date - timedelta(days=13)

    df = crud.event.get_multi(start_date, end_date, event_type=1)
    action_counts = (
        df.groupby("country_id")["article_id"]
        .count()
        .rename("count")
        .drop(-1)
        .reset_index()
    )
    deck, tooltip = country_counts(df_counts=action_counts)
    return deck.to_json(), tooltip


# @app.callback(Output("graph2", "figure"), [Input("urlNoRefresh", "href")])
# def update_figure2(_):
#     return {
#         "layout": GRAPH_LAYOUT,
#         "data": [
#             {
#                 "uid": "45c0a4",
#                 "line": {
#                     "color": "rgb(255, 127, 14)",
#                     "shape": "spline",
#                     "width": 3,
#                 },
#                 "mode": "lines",
#                 "name": "iOS & Android",
#                 "type": "scatter",
#                 "x": [
#                     "2007-12-01",
#                     "2008-12-01",
#                     "2009-12-01",
#                     "2010-12-01",
#                     "2011-12-01",
#                     "2012-12-01",
#                     "2013-12-01",
#                     "2014-12-01",
#                     "2015-12-01",
#                 ],
#                 "y": [
#                     "0",
#                     "45560506.663365364",
#                     "91145081.21192169",
#                     "232447635.15836716",
#                     "580348915.5698586",
#                     "1182888421.2842617",
#                     "1928559640.2194986",
#                     "2578825762.2643065",
#                     "3022276546.8773637",
#                 ],
#             }
#         ],
#     }


# @app.callback(
#     Output("tab1Body", "children"),
#     [Input("urlNoRefresh", "href"), Input("tab1", "value")],
# )
# def update_tab1(_, tabValue):
#     if tabValue == "0":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "rgb(255, 127, 14)",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )
#     elif tabValue == "1":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "red",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )
#     elif tabValue == "2":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "green",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )


# @app.callback(
#     Output("tab2Body", "children"),
#     [Input("urlNoRefresh", "href"), Input("tab2", "value")],
# )
# def update_tab1(_, tabValue):
#     sleep(3)
#     if tabValue == "0":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "rgb(255, 127, 14)",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )
#     elif tabValue == "1":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "red",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )
#     elif tabValue == "2":
#         return dcc.Graph(
#             figure={
#                 "layout": GRAPH_LAYOUT,
#                 "data": [
#                     {
#                         "uid": "45c0a4",
#                         "line": {
#                             "color": "green",
#                             "shape": "spline",
#                             "width": 3,
#                         },
#                         "mode": "lines",
#                         "name": "iOS & Android",
#                         "type": "scatter",
#                         "x": [
#                             "2007-12-01",
#                             "2008-12-01",
#                             "2009-12-01",
#                             "2010-12-01",
#                             "2011-12-01",
#                             "2012-12-01",
#                             "2013-12-01",
#                             "2014-12-01",
#                             "2015-12-01",
#                         ],
#                         "y": [
#                             "0",
#                             "45560506.663365364",
#                             "91145081.21192169",
#                             "232447635.15836716",
#                             "580348915.5698586",
#                             "1182888421.2842617",
#                             "1928559640.2194986",
#                             "2578825762.2643065",
#                             "3022276546.8773637",
#                         ],
#                     }
#                 ],
#             },
#             className="h-100",
#             style={"minHeight": "100px"},
#             responsive=True,
#         )
