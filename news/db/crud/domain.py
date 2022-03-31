from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDDomain(CRUDBase[models.Domain, Session]):
    ...


domain = CRUDDomain(models.Domain, db.SessionLocal)
