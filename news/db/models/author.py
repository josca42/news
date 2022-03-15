from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.sql import func


class Author(Base):
    __tablename__ = "authors"  # type: ignore

    author = Column(String, primary_key=True)
    article_id = Column(Integer, primary_key=True)
