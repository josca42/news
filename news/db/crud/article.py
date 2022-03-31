from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import pandas as pd
from typing import List
from .base import CRUDBase
from news.db import models, db


class CRUDArticle(CRUDBase[models.Article, Session]):
    def not_fetched(self):
        with self.session() as db:
            query = (
                db.query(self.model)
                .filter(self.model.downloaded == 0)
                .filter(self.model.retries < 2)
            )
            df = pd.read_sql_query(query.statement, db.bind)
        return df

    def url_exists(self, url: str):
        with self.session() as db:
            q = db.query(self.model).filter(self.model.url == url)
            exists = db.query(q.exists()).first()
        return exists[0]

    def list_articles_in_db(self) -> set:
        with self.session() as db:
            query = db.query(self.model.id)
            list_of_articles = query.distinct()

        return {article_id[0] for article_id in list_of_articles}

    def get_articles(self, start_date, end_date):
        with self.session() as db:
            query = db.query(self.model).filter(
                self.model.date_publish.between(end_date, start_date)
            )
            df = pd.read_sql_query(query.statement, db.bind)
        return df


article = CRUDArticle(models.Article, db.SessionLocal)
