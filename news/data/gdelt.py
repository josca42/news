import httpx
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from news.data.CONSTANTS import gdel_event_headers
from news.db import crud
from news import config


def add_latest_events2db(english=True):
    url = get_latest_events(english=english)
    fn, df = events_url2df(url)
    add_events2db(df, english=english)

    f_name = f"{fn.split('.')[0]}_{str(english)}.parquet"
    df.to_parquet(config["gdelt_events_dir"] / f_name)


def get_latest_events(english=True):

    if english:
        url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
    else:
        url = "http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt"

    r = httpx.get(url)
    df = pd.read_csv(BytesIO(r.content), sep=" ", names=["f1", "id", "url"])
    url = df["url"].iloc[0]
    return url


def events_url2df(url):
    r = httpx.get(url)
    zipfile = ZipFile(BytesIO(r.content))
    fn = zipfile.namelist()[0]
    df = pd.read_csv(zipfile.open(fn), sep="\t", names=gdel_event_headers)
    return fn, df


def add_events2db(df, english=True):
    for idx, row in df.iterrows():
        article_dict = dict(
            id=row["GLOBALEVENTID"],
            url=row["SOURCEURL"],
            language="en" if english else "trans",
        )
        crud.article.create(article_dict)


if __name__ == "__main__":
    add_latest_events2db(english=True)
