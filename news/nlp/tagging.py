# from booknlp.booknlp import BookNLP
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
