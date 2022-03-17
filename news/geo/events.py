import geopandas as gpd
import pickle

gdf_countries = gpd.read_parquet("countries_simplified.parquet")
gdf_regions = gpd.read_parquet("regions_simplified.parquet")
fips2iso = pickle.load("/Users/josca/projects/1729/news/data/fips2iso.csv")


def create_country_gdf():


def create_regional_gdf():
    df_t["geometry"] = gpd.points_from_xy(df_event["ActionGeo_Lat"], df_event["ActionGeo_Long"])
    t = gdf_event.sjoin(gdf_regions, how="left", predicate="within")



def count(df_events, groupby_col, agg_func, level=""):
    df_counts = (
        df_events.groupby(groupby_col)["GLOBALEVENTID"]
        .count()
        .rename(agg_func)
        .reset_index()
        .assign(GID_0=lambda df: df["ActionGeo_CountryCode"].map(fips2iso))
    )
    return df_counts



gdf_plot = gdf_countries.merge(df_action_counts, on="GID_0", how="inner")

df_event_codes = pd.read_parquet("../data/mappings/CAMEO_event_codes.parquet").rename(columns={"CAMEOEVENTCODE": "EventCode",  "EVENTDESCRIPTION": "event_descr"})
df = df.merge(df_event_codes, on="EventCode", how="left")


