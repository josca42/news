from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import pandas as pd
from typing import List
import pandas as pd

from news.db import models, db


class CRUDArticle:
    def __init__(self, model: models.Article, session: Session):
        """
        **Parameters**

        * `model`: A SQLAlchemy model class
        * `session`: A SQLAlchemy SessionLocal object
        """
        self.model = model
        self.session = session

    def get(self, id: str) -> models.Article:
        with self.session() as db:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
        return db_obj

    def create(self, article_dict: dict) -> None:
        article_obj = self.model(**article_dict)
        with self.session() as db:
            try:
                db.add(article_obj)
                db.commit()
            except IntegrityError:
                db.rollback()

    def update(self, article_update: dict) -> None:
        db_obj = self.get(article_update["id"])

        for field in article_update:
            setattr(db_obj, field, article_update[field])

        with self.session() as db:
            db.add(db_obj)
            db.commit()

    def not_fetched(self):
        with self.session() as db:
            query = (
                db.query(self.model)
                .filter(self.model.downloaded == 0)
                .filter(self.model.retries < 2)
            )
            df = pd.read_sql_query(query.statement, db.bind)
        return df

    def exists(self, id: str):
        with self.session() as db:
            q = db.query(self.model).filter(self.model.id == id)
            exists = db.query(q.exists()).first()
        return exists[0]

    def list_articles_in_db(self, source=None) -> set:
        with self.session() as db:
            query = db.query(self.model.id)
            list_of_articles = query.distinct()

        return {article_id[0] for article_id in list_of_articles}


article = CRUDArticle(models.Article, db.SessionLocal)

if __name__ == "__main__":
    a = article.filter(filters={"language": "en"})
