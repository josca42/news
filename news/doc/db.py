from docarray import DocumentArray
from docarray.array.sqlite import SqliteConfig
from news import config

cfg = SqliteConfig(
    connection=str(config["sqlite_doc_store"]), table_name="raw_documents"
)
doc_store = DocumentArray(storage="sqlite", config=cfg)
