from news.data import io
from news import config
from news.nlp.tagging import get_tags_and_relations
from pathlib import Path
import pandas as pd
from tqdm import tqdm

articles_dir = config["articles_dir"]
ner_dfs, relations_dfs = [], []
for i, fp in tqdm(enumerate(articles_dir.iterdir()), total=207895):
    article_id = int(fp.name.split(".")[0])

    try:
        article = io.json_reader(fp)
        article_text = article["maintext"]

        if (
            article_text is None
            or len(article_text) == 0
            or article["language"] != "en"
        ):
            continue

    except:
        continue

    df_ner, df_relations = get_tags_and_relations(article_text)
    df_ner["id"] = article_id
    df_relations["id"] = article_id
    ner_dfs.append(df_ner)
    relations_dfs.append(df_relations)

    if i % 1000:
        df_ner = pd.concat(ner_dfs)
        df_ner.to_parquet(f"/home/paperspace/src/news/data/tags/df_ner_{i}.parquet")

        df_relations = pd.concat(relations_dfs)
        df_relations.to_parquet(
            f"/home/paperspace/src/news/data/tags/df_relations_{i}.parquet"
        )

        ner_dfs, relations_dfs = [], []
