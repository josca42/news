from sqlalchemy.sql.sqltypes import Boolean
from news.db.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Domain(Base):
    source_domain = Column(String, primary_key=True, index=True, nullable=False)
    country_id = Column(Integer, index=True)
