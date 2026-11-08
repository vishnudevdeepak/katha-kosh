from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    region = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    language = Column(String(100), nullable=True)
    community = Column(String(255), nullable=True)
    historical_period = Column(String(100), nullable=True)
    artisan = Column(String(255), nullable=True)
    storyteller = Column(String(255), nullable=True)
    contributor_name = Column(String(255), nullable=False)
    contributor_email = Column(String(255), nullable=False)
    contributor_role = Column(String(100), nullable=True)  # researcher, community_member, artist, educator
    status = Column(String(20), nullable=False, default="pending", index=True)  # pending, approved, rejected
    review_notes = Column(Text, nullable=True)
    image_paths = Column(Text, nullable=True)  # JSON list of image file paths
    sources = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
