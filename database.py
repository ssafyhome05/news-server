from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

USERNAME = "ssafy"
PASSWORD = "ssafy"
HOST = "localhost"
PORT = "3306"
DBNAME = "zipchack"
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