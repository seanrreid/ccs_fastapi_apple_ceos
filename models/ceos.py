from sqlmodel import Field, Relationship

from .base import Base

class Ceo(Base, table=True):
    __tablename__ = "apple_ceos"

    name: str
    slug: str
    year: int

    def __repr__(self):
        return f"<CEO {self.name!r}>"
