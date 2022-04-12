from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Event(Base):

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True, index=True)
    event_code = Column(String, primary_key=True, index=True, nullable=True)
    country_id = Column(Integer, primary_key=True, index=True, default=-1)
    region_id = Column(Integer, primary_key=True, index=True, default=-1)
    type = Column(Integer, primary_key=True)

    article = relationship("Article")
