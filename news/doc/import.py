from docarray import Document
from news import config
from news.data import io
from datetime import datetime
from news.doc.db import doc_store
from tqdm import tqdm
from news.db import crud


def import_articles2docArray(load_images=False):
    new_articles = crud.article.filter(filters=dict(added2docs=False, downloaded=True))
    articles_dir = config["articles_dir"]

    for article_id in tqdm(new_articles["id"].astype(str), total=len(new_articles)):

        fp = articles_dir / f"{article_id}.json.lz4"
        article = io.json_reader(fp)

        metadata = get_article_meta_data(article=article)
        doc = create_document(
            doc_id=article_id,
            article=article,
            metadata=metadata,
            load_image=load_images,
        )
        doc_store.append(doc)

        crud.article.update(article_update=dict(id=article_id, added2docs=True))


def get_article_meta_data(article: dict) -> dict:
    return dict(
        authors=article["authors"],
        date_download=datetime.fromisoformat(article["date_download"])
        if article["date_download"]
        else None,
        date_publish=datetime.fromisoformat(article["date_publish"])
        if article["date_publish"]
        else None,
        language=article["language"],
        source_domain=article["source_domain"],
    )


def create_document(doc_id, article, metadata, load_image=False):
    title = Document(text=article["title"], tags=dict(section="title"))
    descr = Document(text=article["description"], tags=dict(section="descr"))
    text = Document(text=article["maintext"], tags=dict(section="body"))

    if load_image:
        try:
            image = Document(
                uri=article["image_url"], tags=dict(section="image")
            ).load_uri_to_image_tensor()
        except:
            image = Document(modality="image", tags=dict(section="image"))
    else:
        image = Document(modality="image", tags=dict(section="image"))

    doc = Document(id=doc_id, chunks=[title, descr, text, image], tags=metadata)
    return doc


if __name__ == "__main__":
    import_articles2docArray()
