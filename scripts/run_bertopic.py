from bertopic import BERTopic
import numpy as np
from news import config
from news.data import io
from datetime import datetime

articles_dir = config["articles_dir"]
articles = []
for i, fp in enumerate(articles_dir.iterdir()):

    try:
        article = io.json_reader(fp)
        article_text = article["maintext"]

        if article_text is None or len(article_text) == 0:
            pass
        else:
            articles.append(article_text)

    except:
        continue


topic_model = BERTopic(
    embedding_model="distiluse-base-multilingual-cased-v2", verbose=True
)
topics, probs = topic_model.fit_transform(articles)
arr_topics_probs = np.vstack([np.array(topics), probs]).T

date = datetime.now().strftime("%Y-%m-%d")
np.save(f"/home/paperspace/src/news/data/topics/bertopic_{date}.npy", arr_topics_probs)
topic_model.save(f"/home/paperspace/src/news/data/models/bertopic_{date}")
