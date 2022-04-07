from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from config import settings

# engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
DATABASE_URL = f'mysql+pymysql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'%quote(settings.database_password)
engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
conn = engine.connect()



