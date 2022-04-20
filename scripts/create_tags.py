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

        df_ner, df_relations = get_tags_and_relations(text)

        df_ner["id"] = doc.id
        df_relations["id"] = doc.id

        for idx, row in df_ner.iterrows():
            crud.ner.create(row.to_dict())

        for idx, row in df_relations.iterrows():
            crud.relation.create(row.to_dict())
