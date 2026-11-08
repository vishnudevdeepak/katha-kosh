from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(10), nullable=True, unique=True)
    description = Column(Text, nullable=True)
    item_count = Column(Integer, default=0)
