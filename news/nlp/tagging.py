from booknlp.booknlp import BookNLP
from news.data import io
from pathlib import Path
from news import config
import pandas as pd
from flair.models import SequenceTagger, RelationExtractor
from flair.tokenization import SegtokSentenceSplitter


extractor: RelationExtractor = RelationExtractor.load("relations")
tagger = SequenceTagger.load("ner")
# initialize sentence splitter
splitter = SegtokSentenceSplitter()


# model_params = {"pipeline": "entity,quote,supersense,event,coref", "model": "big"}
# booknlp = BookNLP("en", model_params)


def get_tags_and_relations(text):
    sentences = splitter.split(text)
    tagged_sentences = add_ner_tags(sentences)
    ner_list = extract_tags(tagged_sentences)
    relations_list = extract_relations(tagged_sentences)

    df_ner = count_occurences(ner_list)
    df_relations = count_occurences(relations_list)
    return df_ner, df_relations


def add_ner_tags(sentences):
    tagger.predict(sentences)
    return sentences


def extract_tags(tagged_sentences):
    ner_list = []
    for sentence in tagged_sentences:
        for ner_entitiy in sentence.get_spans():
            ner_list.append(
                {"text": ner_entitiy.text, "label": ner_entitiy.labels[0].value}
            )
    return ner_list


def extract_relations(tagged_sentences):
    relations_list = []
    for sentence in tagged_sentences:
        extractor.predict(sentence)
        relations = sentence.get_labels("relation")

        for relation in relations:
            relations_list.append(
                {
                    "subject": relation.head.text,
                    "predicate": relation.value,
                    "object": relation.tail.text,
                }
            )

    return relations_list


def count_occurences(list_of_dicts):
    if not list_of_dicts:
        return pd.DataFrame()
    else:
        return (
            pd.DataFrame.from_dict(list_of_dicts)
            .reset_index()
            .groupby(list(list_of_dicts[0].keys()))
            .count()
            .rename(columns={"index": "count"})
            .reset_index()
        )


# article_text = article_text.strip("\n").strip("\\")


# Input file to process
# input_file = "/home/paperspace/src/news/data/booknlp2/test.txt"

# # Output directory to store resulting files in
# output_directory = "/home/paperspace/src/news/data/booknlp2/"

# # File within this directory will be named ${book_id}.entities, ${book_id}.tokens, etc.
# book_id = "bartleby"


# def booknlp(text: str):
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         dir_path = Path(tmp_dir)

#         input_file = dir_path / "input_file.txt"
#         with input_file.open("a") as f:
#             f.write(text)

#         booknlp.process(input_file, dir_path, "book")


#         a = 2

#     return True
#     ### Read in results here ###


# if __name__ == "__main__":

#     article = io.json_reader("/home/paperspace/src/news/data/articles/148692.json.lz4")
#     article_text = article["maintext"]

#     booknlp(article_text)
