from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDNer(CRUDBase[models.Ner, Session]):
    ...


ner = CRUDNer(models.Ner, db.SessionLocal)
