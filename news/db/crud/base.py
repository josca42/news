from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from news.db.db.base_class import Base
from sqlalchemy.dialects.sqlite import insert


ModelType = TypeVar("ModelType", bound=Base)
SessionType = TypeVar("SessionType", bound=Session)


class CRUDBase(Generic[ModelType, SessionType]):
    def __init__(self, model: Type[ModelType], session: Type[SessionType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.session = session

    def count(self) -> int:
        with self.session() as db:
            count = db.query(self.model).count()
        return count

    def get(self, id) -> ModelType:
        with self.session() as db:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
        return db_obj

    def create(self, row_dict: dict) -> None:
        row_obj = self.model(**row_dict)
        with self.session() as db:
            try:
                db.add(row_obj)
                db.commit()
            except IntegrityError:
                db.rollback()

    def update(self, row_dict: dict) -> None:
        db_obj = self.get(row_dict["id"])

        for field in row_dict:
            setattr(db_obj, field, row_dict[field])

        with self.session() as db:
            db.add(db_obj)
            db.commit()

    def filter(self, filters: dict) -> pd.DataFrame:
        """
        If multiple filter conditions then the "and" filter operation
        is performed.
        """
        with self.session() as db:
            query = db.query(self.model)
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)

            df = pd.read_sql_query(query.statement, db.bind)
        return df

    def upsert(self, row_dict: dict):
        """
        Function for upserting to sqlite db
        """
        with self.session() as db:
            index_keys = self.model.__table__.primary_key.columns.keys()
            stm = (
                insert(self.model)
                .values(row_dict)
                .on_conflict_do_update(index_elements=index_keys, set_=row_dict)
            )
            db.execute(stm)
            db.commit()
