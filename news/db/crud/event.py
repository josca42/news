from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db
from datetime import datetime
import pandas as pd

Article = models.Article


class CRUDEvent(CRUDBase[models.Event, Session]):
    def get_multi(
        self, start_date: datetime, end_date: datetime, event_type: int = None
    ):
        with self.session() as db:
            query = db.query(self.model)

            if event_type:
                query = query.filter(self.model.type == event_type)

            query = query.join(Article).filter(
                Article.date_publish.between(end_date, start_date)
            )
            df = pd.read_sql_query(query.statement, db.bind)
        return df


event = CRUDEvent(models.Event, db.SessionLocal)
