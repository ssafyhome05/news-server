from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class News(Base):
    __tablename__ = 'news'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dong_code = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    ref = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    city_name = Column(String(50), nullable=False)
    img = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True)