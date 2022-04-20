from news.data import io
from news import config
from news.nlp.tagging import get_tags_and_relations
from news.db.db.doc import doc_store
from news.db import crud
import pandas as pd
from tqdm import tqdm

ner_dfs, relations_dfs = [], []
for doc in doc_store:
    text = doc.chunks.split_by_tag("section")["body"].texts[0]
    language = crud.article.filter(dict(id=doc.id))["language"].squeeze()

    if language == "en":
        

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
