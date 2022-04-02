from bertopic import BERTopic
import numpy as np
from news import config
from news.data import io
from datetime import datetime


def bertopic_fit_transform():
    articles = get_articles_text()

    topic_model = BERTopic(
        embedding_model="distiluse-base-multilingual-cased-v2", verbose=True
    )
    topics, probs = topic_model.fit_transform(articles)
    arr_topics_probs = np.vstack([np.array(topics), probs]).T
    return topic_model, arr_topics_probs


def get_articles_text():
    articles_dir = config["articles_dir"]
    articles = []
    for fp in articles_dir.iterdir():
        try:
            article = io.json_reader(fp)
            article_text = article["maintext"]

            if article_text is None or len(article_text) == 0:
                pass
            else:
                articles.append(article_text)

        except:
            continue

    return articles
