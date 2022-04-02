from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Relation(Base):

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, index=True)
    subject = Column(String)
    predicate = Column(String)
    object = Column(String)
    count = Column(Integer)

    article = relationship("Article")
