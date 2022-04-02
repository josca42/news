from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDQuote(CRUDBase[models.Quote, Session]):
    ...


quote = CRUDQuote(models.Quote, db.SessionLocal)
