# flake8: noqa E501
from time import sleep

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_deck
import pydeck as pdk
from news.db import crud
from news import plot
import dash_bootstrap_components as dbc

from dashboard.app.app import app
from dashboard.app.components.cards import card, grid_card, tab_card
from dashboard.app.components.wrappers import main_wrapper
from datetime import datetime, timedelta
from news import config
from news import plot
import dash_daq as daq
import geopandas as gpd
import pickle


GRAPH_LAYOUT = {"margin": {"t": 10, "l": 20, "r": 20, "b": 20}}
topics_id2name = pickle.load(
    open("/Users/josca/projects/1729/news/data/topics_id2name.p", "rb")
)
gdf_countries = gpd.read_parquet(config["gis_dir"] / "countries_simplified.parquet")[
    ["country", "country_id"]
]
country_dropdown = [
    {"label": label, "value": value} for idx, (label, value) in gdf_countries.iterrows()
]

start_date = datetime.now()
end_date = start_date - timedelta(days=17)


def layout(sidebar_context):

    graph_row1 = html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H6("Country", className="card-title"),
                                dcc.Dropdown(
                                    id="country-id",
                                    options=country_dropdown
                                    + [{"label": "All", "value": "all"}],
                                    value="all",
                                ),
                            ],
                            className="mb-2",
                        ),
                        html.Div(
                            [
                                html.H6("Plot", className="card-title pt-2"),
                                dcc.Dropdown(
                                    id="map-var",
                                    options=[
                                        {
                                            "label": "Url origin",
                                            "value": "domain_country",
                                        },
                                        {"label": "Actors", "value": "actor"},
                                        {"label": "Action", "value": "action"},
                                    ],
                                    value="domain_country",
                                    className="mb-1 pb-1",
                                ),
                            ],
                            className="mb-2",
                        ),
                        html.Div(
                            [
                                html.H6("Settings", className="card-title pt-2"),
                                html.Div(
                                    daq.BooleanSwitch(
                                        id="map-3d",
                                        on=True,
                                        label="3D",
                                        labelPosition="bottom",
                                    ),
                                    className="pb-1",
                                    style={"float": "left"},
                                ),
                                html.Div(
                                    daq.BooleanSwitch(
                                        id="map-regions",
                                        on=False,
                                        label="regions",
                                        labelPosition="bottom",
                                    ),
                                    className="pb-1",
                                    style={"float": "left"},
                                ),
                            ],
                        ),
                    ],
                ),
                color="light",
                className="col-2 h-100",
            ),
            html.Div(
                dcc.Loading(
                    html.Div(
                        dash_deck.DeckGL(
                            id="event-map",
                            mapboxKey=config["MAPBOX_API_KEY"],
                            # enableEvents=True,
                        ),
                    ),
                    parent_className="h-100",
                    color="var(--bs-primary)",
                ),
                className="card col-10 h-100",
            ),
        ],
        className="row flex-grow-1",
    )

    graph_row2 = html.Div(
        [
            html.Div(
                grid_card(
                    "Topics",
                    dcc.Graph(
                        id="topics-ts",
                        className="h-100",
                        style={"minHeight": "100px"},
                        responsive=True,
                    ),
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
            html.Div(
                tab_card(
                    None,
                    id="entities",
                    elements=[
                        {"label": "PER", "value": "PER"},
                        {"label": "ORG", "value": "ORG"},
                    ],
                    value="PER",
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
        ],
        className="row flex-grow-1",
    )

    return main_wrapper(
        [graph_row1, graph_row2],
        sidebar_context,
    )


@app.callback(
    [Output("event-map", "data"), Output("event-map", "tooltip")],
    [Input("urlNoRefresh", "href")],
)
def update_event_map(_):
    df = crud.event.get_multi(start_date, end_date, event_type=1)
    action_counts = (
        df.groupby("country_id")["article_id"]
        .count()
        .rename("count")
        .drop(-1)
        .reset_index()
    )
    deck, tooltip = plot.map.country_counts(df_counts=action_counts)
    return deck.to_json(), tooltip


@app.callback(Output("topics-ts", "figure"), [Input("urlNoRefresh", "href")])
def update_topics(_):
    df_topics = crud.article.get_multi(
        start_date=start_date,
        end_date=end_date,
        columns=["date_publish", "topic"],
        not_equals=dict(topic=-1),
    )

    topics = df_topics["topic"].value_counts().index[:10]
    df_topics = (
        df_topics[df_topics["topic"].isin(topics)]
        .groupby([df_topics["date_publish"].dt.date, "topic"])
        .count()
        .set_axis(["count"], axis=1)
        .reset_index("topic")
    )

    fig = plot.timeseries.base(df_topics, "topic", topics_id2name)
    return fig


@app.callback(
    Output("entitiesBody", "children"),
    [Input("urlNoRefresh", "href"), Input("entities", "value")],
)
def update_entities(_, tabValue):
    def agg_entities(df_ent):
        top_10_ents = df_ent["text"].value_counts().index[:10]
        df_ent = (
            df_ent[df_ent["text"].isin(top_10_ents)]
            .groupby([df_ent["date_publish"].dt.date, "text"])["count"]
            .sum()
            .reset_index("text")
        )
        return df_ent

    if tabValue == "PER":
        df_people = crud.ner.get_multi(
            start_date=start_date,
            end_date=end_date,
            label="PER",
        )
        df_people = agg_entities(df_people)
        fig = plot.timeseries.base(df_people, "text")
        return dcc.Graph(
            figure=fig,
            className="h-100",
            style={"minHeight": "100px"},
            responsive=True,
        )
    elif tabValue == "ORG":
        df_org = crud.ner.get_multi(
            start_date=start_date,
            end_date=end_date,
            label="ORG",
        )
        df_org = agg_entities(df_org)
        fig = plot.timeseries.base(df_org, "text")
        return dcc.Graph(
            figure=fig,
            className="h-100",
            style={"minHeight": "100px"},
            responsive=True,
        )
