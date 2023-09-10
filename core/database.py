from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_host = "localhost"
db_port = "5455"
db_name = "test"
db_user = "test"
db_password = "P@ssw0rd"

DATABASE_URL = "postgresql://ydhmodfa:cwqT-7fm7vUS452jNp2H54jToJZEjHD8@satao.db.elephantsql.com/ydhmodfa"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

