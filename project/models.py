from database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__="Users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(200))
    email=Column(String(200))
    age=Column(Integer)
    password=Column(String(200))

