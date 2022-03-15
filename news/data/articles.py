from newsplease import NewsPlease
from news.db import crud
from news import config
from news.data import io
from concurrent.futures import ProcessPoolExecutor
from wrapt_timeout_decorator import timeout


def fetch_new_articles():
    chunk_size = 20
    articles = crud.article.not_fetched()
    pool = ProcessPoolExecutor(5)
    chunks = (len(articles) // chunk_size) + 1
    chunked_data = [
        articles[idx * chunk_size : (idx + 1) * chunk_size] for idx in range(chunks)
    ]
    pool.map(fetch_articles, chunked_data)
    pool.shutdown()


def fetch_articles(articles):
    for idx, article in articles.iterrows():
        url, Id = article["url"], article["id"]
        try:
            article_obj = fetch(url)
            save(article_obj, article_id=Id)

            crud.article.update(dict(id=Id, downloaded=1))
        except:
            retries = article["retries"] + 1
            crud.article.update(dict(id=Id, retries=retries))


@timeout(20)
def fetch(url):
    return NewsPlease.from_url(url)


def save(article_obj, article_id):
    fp = config["articles_dir"] / f"{article_id}.json.lz4"
    io.json_writer(fp, article_obj.get_dict())


if __name__ == "__main__":
    fetch_new_articles()
