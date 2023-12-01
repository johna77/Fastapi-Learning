from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2, time
from psycopg2.extras import RealDictCursor
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DB_CONFIG = {
#     'user': 'postgres',
#     'password': 'johnajohna',
#     'host': 'localhost',
#     'port': '5432',
#     'database': 'fastapi',
# }

# while True:
#     try:
#         conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("DB is successfully connected")
#         break
#     except Exception as error:
#         print("Connecting to db failed!!!")
#         print("Error: ", error)
#         time.sleep(2)