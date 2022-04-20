import pandas as pd
from sqlalchemy import create_engine
from news.db import crud
from tqdm import tqdm

SQLALCHEMY_DATABASE_URI = f"sqlite:////root/news/data/archive/db/sqlite_articles.db"
articles_old_db = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

df = pd.read_sql_table("articles", con=articles_old_db)
df = (
    df.drop(columns=["added2docs", "indexed"])
    .rename(columns={"time_created": "timestamp"})
    .copy()
)

for idx, row in tqdm(df.iterrows(), total=len(df)):
    crud.article.create(row_dict=row.to_dict())
