import geopandas as gpd
import pickle
from news import config
from news.db import crud
import pandas as pd
from tqdm import tqdm
import numpy as np

gdf_regions = gpd.read_parquet(
    "/Users/josca/projects/1729/news/data/gis/regions_simplified.parquet"
)


def add_new_events():
    new_events = crud.article.filter(filters=dict(events_added=False, downloaded=True))
    new_event_files = new_events["gdelt_fn"].unique()
    url2article_id = new_events.set_index("url").sort_index()["id"]
    for fn in tqdm(new_event_files):
        fp = config["gdelt_events_dir"] / fn
        df_events = pd.read_parquet(fp)
        df_events = add_region_cols(df_events)

        for url, article_events in df_events.groupby("SOURCEURL"):
            if url in url2article_id:
                df_extracted_events = extract_events_for_article(article_events)
                article_id = url2article_id[url]
                for idx, event_row in df_extracted_events.iterrows():
                    add_events2db(event_dict=event_row.to_dict(), article_id=article_id)

                    crud.article.update(
                        row_dict=dict(
                            id=int(article_id),
                            events_added=True,
                        )
                    )
            else:
                continue


def add_region_cols(df_events):
    entity_cols = ["Actor1Geo", "Actor2Geo", "ActionGeo"]
    for entity_col in entity_cols:
        gdf_events = gpd.GeoDataFrame(
            df_events["GLOBALEVENTID"],
            geometry=gpd.points_from_xy(
                df_events[f"{entity_col}_Long"], df_events[f"{entity_col}_Lat"]
            ),
            crs="EPSG:4326",
        )
        gdf_events = gdf_events.sjoin(gdf_regions, how="left", predicate="within")
        gdf_events = gdf_events.rename(
            columns={
                "region_id": f"{entity_col}_region",
                "country_id": f"{entity_col}_country",
            }
        )
        df_events = df_events.merge(
            gdf_events[
                ["GLOBALEVENTID", f"{entity_col}_region", f"{entity_col}_country"]
            ],
            on="GLOBALEVENTID",
        )
    return df_events


def extract_events_for_article(df_article):
    actor_geo = []
    action_geo = []
    entity_cols = ["Actor1Geo", "Actor2Geo", "ActionGeo"]
    geo_cols = ["Actor1Geo_ADM1Code", "Actor2Geo_ADM1Code", "Action2Geo_ADM1Code"]
    for entity_col in entity_cols:
        for idx, (geo_code, region_id, country_id, event_code) in df_article[
            [
                f"{entity_col}_ADM1Code",
                f"{entity_col}_region",
                f"{entity_col}_country",
                "EventCode",
            ]
        ].iterrows():

            if geo_code is None:
                continue

            if len(geo_code) == 2:
                region_id = None

            if "actor" in entity_col.lower():
                actor_geo.append(
                    {"country_id": country_id, "region_id": region_id, "type": 0}
                )
            else:
                action_geo.append(
                    {
                        "country_id": country_id,
                        "region_id": region_id,
                        "event_code": event_code,
                        "type": 1,
                    }
                )

    df_actor_geo = pd.DataFrame(actor_geo).drop_duplicates()
    df_action_geo = pd.DataFrame(action_geo).drop_duplicates()
    return pd.concat([df_actor_geo, df_action_geo])


def add_events2db(event_dict: dict, article_id: int) -> None:
    event_dict["article_id"] = int(article_id)
    for geo_key in ["country_id", "region_id"]:
        val = event_dict[geo_key] if event_dict[geo_key] else np.nan
        if np.isnan(val):
            event_dict[geo_key] = -1
        else:
            event_dict[geo_key] = int(event_dict[geo_key])

    crud.event.create(row_dict=event_dict)


if __name__ == "__main__":
    add_new_events()
