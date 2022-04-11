from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db
from datetime import datetime
import pandas as pd

Article = models.Article


class CRUDNer(CRUDBase[models.Ner, Session]):
    def get_multi(
        self,
        start_date: datetime,
        end_date: datetime,
        label: str = None,
        columns: list = [],
    ):
        with self.session() as db:
            query = db.query(self.model, Article.date_publish)

            if label:
                query = query.filter(self.model.label == label)

            if columns:
                query = self._select_columns(query, columns)

            query = query.join(Article).filter(
                Article.date_publish.between(end_date, start_date)
            )
            df = pd.read_sql_query(query.statement, db.bind)
        return df


ner = CRUDNer(models.Ner, db.SessionLocal)
