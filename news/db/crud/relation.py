from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDRelation(CRUDBase[models.Relation, Session]):
    ...


relation = CRUDRelation(models.Relation, db.SessionLocal)
