from newsplease import NewsPlease
from news.db import crud
from news import config
from news.data import io
from concurrent.futures import ProcessPoolExecutor


def fetch(article):
    try:
        article_obj = NewsPlease.from_url(article["url"])

        fp = config["articles_dir"] / f"{article['id']}.json.lz4"
        io.json_writer(fp, article_obj.get_dict())

        crud.article.update(dict(id=article["id"], downloaded=1))
    except:
        retries = article["retries"] + 1
        crud.article.update(dict(id=article["id"], retries=retries))


def fetch_articles(articles):
    for idx, article in articles.iterrows():
        fetch(article)


def fetch_remaining():
    chunk_size = 20
    articles = crud.article.not_fetched()
    pool = ProcessPoolExecutor(20)
    chunks = (len(articles) // chunk_size) + 1
    chunked_data = [
        articles[idx * chunk_size : (idx + 1) * chunk_size] for idx in range(chunks)
    ]
    pool.map(fetch_articles, chunked_data)
    pool.shutdown()


if __name__ == "__main__":
    fetch_remaining()
