from operator import index
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
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    gdelt_fn = Column(String)
    downloaded = Column(Boolean, default=False)
    article_processed = Column(Boolean, default=False)
    events_added = Column(Boolean, default=False)
    indexed = Column(Boolean, default=False)
    language = Column(String, default=None, nullable=True)
    retries = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    topic = Column(Integer, nullable=True)
    date_download = Column(DateTime(timezone=False), nullable=True)
    date_publish = Column(
        DateTime(timezone=False), nullable=False, server_default=func.now(), index=True
    )
    source_domain = Column(String, default=None, nullable=True)
    domain_country = Column(Integer, default=None, nullable=True, index=True)
