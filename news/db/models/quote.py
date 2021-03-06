from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Quote(Base):

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, index=True)
    quote = Column(String, primary_key=True, index=False)
    quotee = Column(String, primary_key=True, index=True)

    article = relationship("Article")
