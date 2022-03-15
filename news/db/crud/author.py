from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import pandas as pd
from typing import List
import pandas as pd

from news.db import models, db


class CRUDAuthor:
    def __init__(self, model: models.Author, session: Session):
        """
        **Parameters**

        * `model`: A SQLAlchemy model class
        * `session`: A SQLAlchemy SessionLocal object
        """
        self.model = model
        self.session = session

    def get(self, author: str) -> models.Author:
        with self.session() as db:
            db_obj = db.query(self.model).filter(self.model.author == author).first()
        return db_obj

    def create(self, author: str, article_id: int) -> None:
        article_obj = self.model(author=author, article_id=article_id)
        with self.session() as db:
            try:
                db.add(article_obj)
                db.commit()
            except IntegrityError:
                db.rollback()


author = CRUDAuthor(models.Author, db.SessionLocal)
