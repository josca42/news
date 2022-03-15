from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import (
    Column,
    Float,
    BigInteger,
    Integer,
    String,
    Boolean,
    null,
    DateTime,
)
from sqlalchemy.sql import func


class Article(Base):
    __tablename__ = "articles"  # type: ignore

    id = Column(Integer, primary_key=True)
    url = Column(String)
    gdelt_fn = Column(String)
    downloaded = Column(Boolean, default=0)
    added2docs = Column(Boolean, default=0)
    indexed = Column(Boolean, default=0)
    language = Column(String, default="")
    retries = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
