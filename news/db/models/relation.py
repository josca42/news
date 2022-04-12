from operator import index
from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Relation(Base):

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, index=True)
    subject = Column(String, primary_key=True, index=False)
    predicate = Column(String, primary_key=True, index=False)
    object = Column(String, primary_key=True, index=False)
    count = Column(Integer)

    article = relationship("Article")
