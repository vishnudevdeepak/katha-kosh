from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class HeritageItem(Base):
    __tablename__ = "heritage_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False, index=True)  # folk_story, craft, folk_art, textile, pottery, woodwork, metalwork, dance, music, ritual, oral_history
    region = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=True)
    language = Column(String(100), nullable=True)
    community = Column(String(255), nullable=True)
    historical_period = Column(String(100), nullable=True)
    cultural_significance = Column(Text, nullable=True)
    traditional_technique = Column(Text, nullable=True)
    why_it_matters = Column(Text, nullable=True)
    preservation_status = Column(String(50), nullable=True)  # thriving, vulnerable, endangered, critically_endangered
    artisan = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="published", index=True)  # published, pending, rejected
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # comma-separated
    sources = Column(Text, nullable=True)
    embedding_id = Column(String(100), nullable=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
