from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("heritage_items.id"), nullable=True, index=True)
    contribution_id = Column(Integer, ForeignKey("contributions.id"), nullable=True, index=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # image, audio, video, document
    mime_type = Column(String(100), nullable=True)
    original_filename = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
