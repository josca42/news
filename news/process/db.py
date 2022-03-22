from docarray import DocumentArray
from docarray.array.sqlite import SqliteConfig
from news import config
from datetime import datetime

# from annlite import AnnLite

cfg = SqliteConfig(
    connection=str(config["sqlite_doc_store"]), table_name="raw_documents"
)
doc_store = DocumentArray(storage="sqlite", config=cfg)


# indexer_title = AnnLite(
#     dim=768,
#     columns=[("date", datetime), ("source", str), ("lang", str)],
#     data_path=config["db_data_dir"] / "title_annlite",
# )
