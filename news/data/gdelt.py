import httpx
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from news.data.CONSTANTS import gdel_event_headers
from news.db import crud
from news import config
from tqdm import tqdm


def add_latest_events2db(english=True):
    url = get_latest_events(english=english)
    fn, df = events_url2df(url)
    fn = f"{fn.split('.')[0]}_{str(english)}.parquet"
    add_events2db(df, fn=fn)

    df.to_parquet(config["gdelt_events_dir"] / fn)


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
    df = pd.read_csv(
        zipfile.open(fn),
        sep="\t",
        names=gdel_event_headers,
        dtype={"EventCode": str, "EventBaseCode": str, "EventRootCode": str},
    )
    return fn, df


def add_events2db(df, fn):
    for url in df["SOURCEURL"].unique():
        if not crud.article.url_exists(url=url):
            article_dict = dict(url=url, gdelt_fn=fn)
            crud.article.create(article_dict)
        else:
            pass


def recover_events_from_folder():
    events_dir = config["gdelt_events_dir"]
    for fp in tqdm(events_dir.iterdir()):
        df = pd.read_parquet(fp)
        for url in df["SOURCEURL"].unique():
            if not crud.article.url_exists(url=url):
                article_dict = dict(url=url, gdelt_fn=fp.name)
                crud.article.create(article_dict)
            else:
                pass


if __name__ == "__main__":
    recover_events_from_folder()
