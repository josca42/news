from news.db.db.doc import doc_store, doc_index
from news.db import crud
from tqdm import tqdm
from datetime import datetime
from news.nlp.embedding import get_embedding
from docarray import Document, DocumentArray
from news import config


def index_docs():
    def _index_docs(docs):
        docs = DocumentArray(docs)
        doc_index.index(docs)

    new_docs = crud.article.filter(filters=dict(article_processed=True, indexed=False))

    docs = []
    for idx, row in tqdm(new_docs.iterrows(), total=len(new_docs)):
        doc = doc_store[str(row["id"])]

        text = get_section_text(doc)
        embedding = get_embedding(text)

        doc = Document(
            id=str(doc.id),
            embedding=embedding,
            tags={
                "timestamp": row["timestamp"],
                "source_domain": row["source_domain"],
                "language": row["language"],
                "domain_country": row["domain_country"],
            },
        )

        docs.append(doc)
        crud.article.update(row_dict=dict(id=row["id"], indexed=True))

        if idx % 100 == 0 and idx > 1:
            _index_docs(docs)
            docs = []

    if docs:
        _index_docs(docs)


def get_section_text(doc):
    sections = doc.chunks.split_by_tag("section")
    descr = sections["descr"].texts[0]
    if descr != "":
        return descr
    else:
        return sections["title"].texts[0]


if __name__ == "__main__":
    index_docs()
