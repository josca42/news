from pydoc import Doc
from news.doc.db import doc_store
from news.db import crud
from annlite import AnnLite
from tqdm import tqdm
from datetime import datetime
from news.nlp.embedding import get_embedding
from docarray import Document, DocumentArray
from news import config

indexer = AnnLite(
    dim=768,
    columns=[("date", datetime), ("source", str), ("lang", str)],
    data_path=config["db_data_dir"] / "title_annlite",
)


def index_docs():
    def index_docs(docs):
        docs = DocumentArray(docs)
        indexer.index(docs)

    new_docs = crud.article.filter(filters=dict(added2docs=True, indexed=False))

    docs = []
    for i, doc_id in tqdm(enumerate(new_docs["id"].astype(str)), total=len(new_docs)):
        doc = doc_store[doc_id]

        text = get_section_text(doc=doc, section="title")
        embedding = get_embedding(text)

        doc = Document(
            id=doc.id,
            embedding=embedding,
            tags={
                "date": doc.tags["date_publish"],
                "source": doc.tags["source_domain"],
                "lang": doc.tags["language"],
            },
        )

        docs.append(doc)
        crud.article.update(article_update=dict(id=doc.id, indexed=True))

        if i % 100:
            index_docs(docs)
            docs = []

    if docs:
        index_docs(docs)


def get_section_text(doc, section):
    texts = doc.chunks.split_by_tag("section")[section].texts
    return texts[0]


if __name__ == "__main__":
    index_docs()
