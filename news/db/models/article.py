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

    id = Column(BigInteger, primary_key=True, nullable=False)
    url = Column(String)
    downloaded = Column(Boolean, default=0)
    doc_store_raw = Column(Boolean, default=0)
    language = Column(String, default="")
    retries = Column(Integer, default=0)

    time_created = Column(DateTime(timezone=True), server_default=func.now())

    ## Add an extra column that timestamps when each
    ## observation is saved to db table
