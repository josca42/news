from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDAuthor(CRUDBase[models.Author, Session]):
    ...


author = CRUDAuthor(models.Author, db.SessionLocal)
