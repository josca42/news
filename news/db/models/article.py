from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Float, BigInteger, Integer, String, Boolean, null


class Article(Base):
    __tablename__ = "articles"  # type: ignore

    id = Column(BigInteger, primary_key=True, nullable=False)
    url = Column(String)
    downloaded = Column(Boolean, default=0)
    language = Column(String, default="")
    retries = Column(Integer, default=0)

    ## Add an extra column that timestamps when each
    ## observation is saved to db table
