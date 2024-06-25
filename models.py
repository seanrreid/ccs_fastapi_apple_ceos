from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from db_connect import engine
from pydantic import BaseModel

Base = declarative_base()

class CEO(Base):
    __tablename__ = "apple_ceos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    year = Column(Integer)

class CEOCreate(BaseModel):
    name: str
    slug: str
    year: int


Base.metadata.create_all(engine)
