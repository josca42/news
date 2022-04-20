from docarray import DocumentArray
from docarray.array.sqlite import SqliteConfig
from news import config
from datetime import datetime
from annlite import AnnLite

cfg = SqliteConfig(
    connection=str(config["sqlite_doc_store"]), table_name="raw_documents"
)
doc_store = DocumentArray(storage="sqlite", config=cfg)


doc_index = AnnLite(
    dim=512,
    columns=[
        ("timestamp", datetime),
        ("source_domain", str),
        ("language", str),
        ("domain_country", int),
    ],
    data_path=config["db_data_dir"] / "doc_descr_index",
)
