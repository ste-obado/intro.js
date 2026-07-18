from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:password2007@localhost:3306/school"

engine = create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
