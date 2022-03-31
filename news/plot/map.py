import pydeck as pdk
from news.plot.color import generate_color_values
from news import config
import geopandas as gpd
import pandas as pd


gdf_countries = gpd.read_parquet(config["gis_dir"] / "countries_simplified.parquet")


def country_counts(df_counts: pd.DataFrame):

    gdf_plot = gdf_countries.merge(df_counts, on="country_id", how="inner")
    gdf_plot["color"] = generate_color_values(gdf_plot["count"], "plasma", 100)

    view = pdk.ViewState(
        **{"latitude": 48.3794, "longitude": 31.1656, "zoom": 4, "pitch": 45}
    )

    polygon_layer = pdk.Layer(
        "GeoJsonLayer",
        data=gdf_plot,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="count",
        elevation_scale=100,
        get_fill_color="color",
        get_line_color=[0, 0, 0],
        auto_highlight=True,
        pickable=True,
    )

    tooltip = {
        "html": "Country: {country} <br/>" "Count: {count} <br/>",
        "style": {"backgroundColor": "steelblue", "color": "white"},
    }

    deck = pdk.Deck(
        [polygon_layer],
        initial_view_state=view,
        map_style=pdk.map_styles.LIGHT,
    )
    return deck, tooltip
