from dotenv import dotenv_values
from pathlib import Path

config = dotenv_values()
data_dir = Path(config["DATA_DIR"])
# mount_data_dir = Path(config["MOUNT_DATA_DIR"])
config["db_data_dir"] = data_dir / "db"
config["sqlite_db_fp"] = data_dir / "db" / "sqlite_articles.db"
config["sqlite_doc_store"] = data_dir / "db" / "document_store.sqlite"
config["articles_dir"] = data_dir / "articles"
config["gdelt_events_dir"] = data_dir / "gdelt_events"
config["gis_dir"] = data_dir / "gis"
