from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Ner(Base):

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, index=True)
    text = Column(String, primary_key=True)
    label = Column(String, primary_key=True)
    count = Column(Integer)

    article = relationship("Article")
