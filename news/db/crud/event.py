from sqlalchemy.orm import Session
from .base import CRUDBase
from news.db import models, db


class CRUDEvent(CRUDBase[models.Event, Session]):
    ...


event = CRUDEvent(models.Event, db.SessionLocal)
