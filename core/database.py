from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2

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

# create_user_table_query = """
#     CREATE TABLE IF NOT EXISTS users (
#         id SERIAL PRIMARY KEY,
#         username VARCHAR(255) NOT NULL,
#         email VARCHAR(255) NOT NULL UNIQUE
#     );
# """

# create_card_table_query = """
#     CREATE TABLE IF NOT EXISTS card (
#         id SERIAL PRIMARY KEY,
#         card_number VARCHAR(16) NOT NULL,
#         user_id INT REFERENCES users(id)
#     );
# """
# create_history_table_query = """
#     CREATE TABLE IF NOT EXISTS histroy (
#         id SERIAL PRIMARY KEY,
#         date TIMESTAMP NOT NULL,
#         user_id INT REFERENCES users(id)
#     );
# """

# create_attendant_table_query = """
#     CREATE TABLE IF NOT EXISTS attendant (
#         id SERIAL PRIMARY KEY,
#         date TIMESTAMP NOT NULL,
#         user_id INT REFERENCES users(id)
#     );
# """

# try:
#     conn = psycopg2.connect(
#         dbname=db_name,
#         user=db_user,
#         password=db_password,
#         host=db_host,
#         port=db_port
#     )
#     cursor = conn.cursor()
#     cursor.execute(create_user_table_query)
#     cursor.execute(create_card_table_query)
#     cursor.execute(create_history_table_query)
#     cursor.execute(create_attendant_table_query)
#     conn.commit()
#     print("successfully ")

# except psycopg2.Error as e:
#     print("Error:", e)

# finally:
#     cursor.close()
#     conn.close()