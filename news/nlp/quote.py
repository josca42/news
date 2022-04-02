import re
import pandas as pd
import tempfile
from pathlib import Path

# model_params = {"pipeline": "entity,quote,supersense,event,coref", "model": "big"}
# booknlp = BookNLP("en", model_params)

with open("/Users/josca/projects/1729/news/data/nlp/stopwords.text") as f:
    stopwords = f.read().split("\n")


def char_id2quotee(char_id, df_ents):
    names_possible = df_ents[
        (df_ents["COREF"] == char_id)
        & (df_ents["text"].str.lower().isin(stopwords) == False)
    ]
    if names_possible.empty:
        return "unknown"
    else:
        return names_possible["text"].value_counts().index[0]


def add_quotee(df_quotes, df_ents):
    char_id2quotee_mapping = {}
    for char_id in df_quotes["char_id"].unique():
        char_id2quotee_mapping[char_id] = char_id2quotee(char_id, df_ents)
    df_quotes["quotee"] = df_quotes["char_id"].map(char_id2quotee_mapping)
    return df_quotes


def get_article_quotes(dir_path):
    df_quotes = pd.read_csv(dir_path / "book.quotes", sep="\t")
    df_ents = pd.read_csv(dir_path / "book.entities", sep="\t")
    df_quotes = add_quotee(df_quotes, df_ents)
    return df_quotes


# def extract_quotes(text):
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         dir_path = Path(tmp_dir)

#         input_file = dir_path / "input_file.txt"
#         with input_file.open("a") as f:
#             f.write(text)

#         booknlp.process(input_file, dir_path, "book")

#         df_quotes = get_article_quotes(dir_path)

#     return df_quotes
