from newsplease import NewsPlease
from news.db import crud
from news import config
from news.data import io
from anyio import sleep, create_task_group, run
from concurrent.futures import ProcessPoolExecutor


async def fetch(article):
    try:
        article_obj = NewsPlease.from_url(article["url"])

        fp = config["articles_dir"] / f"{article['id']}.json.lz4"
        io.json_writer(fp, article_obj.get_dict())

        crud.article.update(dict(id=article["id"], downloaded=1))
    except:
        retries = article["retries"] + 1
        crud.article.update(dict(id=article["id"], retries=retries))


async def fetch_articles(articles):

    async with create_task_group() as tg:
        for idx, article in articles.iterrows():
            tg.start_soon(fetch, article)


def run_fetch_articles(articles):
    run(fetch_articles, articles)


def fetch_remaining():
    chunk_size = 200
    articles = crud.article.not_fetched()
    pool = ProcessPoolExecutor(4)
    chunks = (len(articles) // chunk_size) + 1
    chunked_data = [
        articles[idx * chunk_size : (idx + 1) * chunk_size] for idx in range(chunks)
    ]

    for _ in pool.map(run_fetch_articles, chunked_data):
        pass

    pool.shutdown()
