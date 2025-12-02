from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import settings

DATABASE_URL = f"mysql+mysqlconnector://{settings.database.user}:{settings.database.password}" \
               f"@{settings.database.host}:3306/{settings.database.name}"

# Engine e sessão
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_connection():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except OperationalError as e:
        print(f"Erro de conexão com o banco: {e}")
        return False
