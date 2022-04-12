# flake8: noqa E501
from time import sleep

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table

from dashboard.app.app import app
from dashboard.app.components.cards import card, grid_card, tab_card
from dashboard.app.components.wrappers import main_wrapper
from news.kg.wikidata import map_rdf_subject2wikidata_link

GRAPH_LAYOUT = {"margin": {"t": 10, "l": 20, "r": 20, "b": 20}}
df_article_rdfs = pd.read_parquet(
    "/Users/josca/projects/1729/news/notebooks/relation_example.parquet"
)
df_quotes = pd.read_parquet(
    "/Users/josca/projects/1729/news/notebooks/quote_example.parquet"
)


def layout(sidebar_context):

    graph_row1 = html.Div(
        [
            html.Div(
                html.Embed(
                    src="https://www.jdsupra.com/legalnews/russian-sanctions-export-controls-3879898/",
                    className="h-100",
                ),
                className="col-12 col-md-3 pt-2 pb-4",
            ),
            html.Div(
                grid_card(
                    "RDF's with links to wikidata knowledge graph",
                    dash_table.DataTable(
                        id="rdf-table",
                        columns=[
                            {"id": name, "name": name}
                            for name in [
                                "subject",
                                "predicate",
                                "object",
                            ]
                        ]
                        + [
                            {
                                "id": "wikidata_link",
                                "name": "wikidata link",
                                "presentation": "markdown",
                            }
                        ],
                        style_as_list_view=True,
                        style_cell={
                            "textAlign": "left",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "backgroundColor": "white",
                            "font-family": "Kanit ExtraLight",
                            "width": "100px",
                            "maxWidth": "100px",
                            "minWidth": "100px",
                        },
                        style_header={
                            "backgroundColor": "#f8f8ff",
                            "font-family": "Kanit Light",
                            "font-weight": "bold",
                        },
                        page_current=0,
                        page_size=10,
                        page_action="custom",
                    ),
                ),
                className="col-12 col-md-9 h-100 pt-2 pb-4",
            ),
        ],
        className="row flex-grow-1",
    )

    graph_row2 = html.Div(
        [
            html.Div(
                grid_card(
                    "Graph",
                    dash_table.DataTable(
                        id="quote-table",
                        data=df_quotes.to_dict("records"),
                        columns=[
                            {"id": name, "name": name}
                            for name in [
                                "quotee",
                                "quote",
                            ]
                        ],
                        tooltip_data=[
                            {"quote": {"value": quote, "type": "markdown"}}
                            for quote in df_quotes["quote"]
                        ],
                        style_as_list_view=True,
                        style_cell={
                            "textAlign": "left",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "backgroundColor": "white",
                            "font-family": "Kanit ExtraLight",
                            "width": "100px",
                            "maxWidth": "100px",
                            "minWidth": "100px",
                        },
                        style_header={
                            "backgroundColor": "#f8f8ff",
                            "font-family": "Kanit Light",
                            "font-weight": "bold",
                        },
                        style_table={"height": "300px", "overflowY": "auto"},
                        tooltip_delay=0,
                        tooltip_duration=None,
                    ),
                ),
                className="col-12 col-md-6 pt-2 pb-4",
            ),
            html.Div(
                grid_card(
                    "Graph",
                    dcc.Graph(
                        id="graph2",
                        figure={"layout": GRAPH_LAYOUT, "data": []},
                        className="h-100",
                        style={"minHeight": "100px"},
                        responsive=True,
                    ),
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
    Output("rdf-table", "data"),
    [Input("rdf-table", "page_current"), Input("rdf-table", "page_size")],
)
def update_event_map(page_current, page_size):
    df_table = df_article_rdfs.iloc[
        page_current * page_size : (page_current + 1) * page_size
    ]
    wikidata_links = map_rdf_subject2wikidata_link(df_table["subject"])
    markdown_col = []
    for link, subject in zip(wikidata_links, df_table["subject"]):
        markdown_col.append(f"[{subject}]({link})" if link else "")

    df_table["wikidata_link"] = markdown_col
    return df_table.to_dict("records")
