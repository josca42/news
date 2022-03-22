from docarray import Document
from news import config
from news.data import io
from datetime import datetime
from news.process.db import doc_store
from tqdm import tqdm
from news.db import crud
from wrapt_timeout_decorator import timeout
import whois


def add_new_articles2tables(recover_db=False):

    new_articles = crud.article.filter(
        filters=dict(article_processed=False, downloaded=False)
    )
    articles_dir = config["articles_dir"]

    for article_id in tqdm(new_articles["id"].astype(str), total=len(new_articles)):

        fp = articles_dir / f"{article_id}.json.lz4"
        article = io.json_reader(fp)

        metadata = get_article_meta_data(article=article)
        add_authors2db(article=article, article_id=article_id)
        add_metadata2db(metadata=metadata, article_id=article_id)
        add_domain_country2db(article, article_id)

        if recover_db:
            pass
        else:
            add_article2doc_store(
                article=article,
                article_id=article_id,
                metadata=metadata,
                load_image=True,
            )

        crud.article.update(
            row_dict=dict(
                id=article_id,
                article_processed=True,
            )
        )


def add_article2doc_store(article, article_id, metadata, load_image=False):
    doc = create_document(
        doc_id=article_id,
        article=article,
        metadata=metadata,
        load_image=load_image,
    )
    doc_store.append(doc)


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
            image = load_image(article)
        except:
            image = Document(modality="image", tags=dict(section="image"))
    else:
        image = Document(modality="image", tags=dict(section="image"))

    doc = Document(id=doc_id, chunks=[title, descr, text, image], tags=metadata)
    return doc


@timeout(20)
def load_image(article):
    return Document(
        uri=article["image_url"], tags=dict(section="image")
    ).load_uri_to_image_tensor()


def add_authors2db(article, article_id):
    for author in article["authors"]:
        row_dict = dict(author=author, article_id=article_id)
        crud.author.create(row_dict)


def add_metadata2db(metadata, article_id):
    authors = metadata.pop("authors")
    metadata["id"] = article_id

    # If date published is None remove from dict
    # so as not to update table with NULL value instead
    # instead of the default server timestamp.
    if metadata["date_publish"] is None:
        del metadata["date_publish"]

    crud.article.update(row_dict=metadata)


def add_domain_country2db(article, article_id):
    source_domain = article["source_domain"]
    domain_country = get_likely_domain_country(source_domain)
    domain_update = dict(id=article_id, domain_country=domain_country)
    crud.article.update(row_dict=domain_update)


def get_likely_domain_country(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info["country"]
    except:
        return None


if __name__ == "__main__":
    add_new_articles2tables(recover_db=True)
