from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config.spring_config import SpringConfigClient

# Config Server에서 설정 가져오기
config_client = SpringConfigClient()

# 데이터베이스 설정 가져오기
USERNAME = config_client.get_property('spring.datasource.username')
PASSWORD = config_client.get_property('spring.datasource.password')
HOST = config_client.get_property('spring.datasource.host')
PORT = config_client.get_property('spring.datasource.port')
DBNAME = config_client.get_property('spring.datasource.database')

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
    
    def get_db():
        db = sessionmaker()
        try:
            yield db
        finally:
            db.close()