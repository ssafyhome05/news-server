from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id          = Column(Integer, primary_key=True, index=True)
    dong_code   = Column(String(50),  nullable=False)
    title       = Column(String(100), nullable=False)
    url         = Column(String(100), nullable=False)
    city_name   = Column(String(50),  nullable=False)
    ref         = Column(String(100), nullable=False)
    img         = Column(String(100), nullable=True)