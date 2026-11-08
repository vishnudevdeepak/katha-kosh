from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HeritageItemBase(BaseModel):
    title: str
    description: str
    type: str
    region: str
    state: str
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    cultural_significance: Optional[str] = None
    traditional_technique: Optional[str] = None
    why_it_matters: Optional[str] = None
    preservation_status: Optional[str] = None
    artisan: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    tags: Optional[str] = None  # comma-separated string input
    sources: Optional[str] = None


class HeritageItemCreate(HeritageItemBase):
    slug: Optional[str] = None  # auto-generated if not provided
    status: str = "published"


class HeritageItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    cultural_significance: Optional[str] = None
    traditional_technique: Optional[str] = None
    why_it_matters: Optional[str] = None
    preservation_status: Optional[str] = None
    artisan: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    tags: Optional[str] = None
    sources: Optional[str] = None


class HeritageItemResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    type: str
    region: str
    state: str
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    cultural_significance: Optional[str] = None
    traditional_technique: Optional[str] = None
    why_it_matters: Optional[str] = None
    preservation_status: Optional[str] = None
    artisan: Optional[str] = None
    status: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    tags: List[str] = []  # split from comma-separated
    sources: Optional[str] = None
    embedding_id: Optional[str] = None
    view_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_tags(cls, item):
        data = {
            "id": item.id,
            "title": item.title,
            "slug": item.slug,
            "description": item.description,
            "type": item.type,
            "region": item.region,
            "state": item.state,
            "district": item.district,
            "language": item.language,
            "community": item.community,
            "historical_period": item.historical_period,
            "cultural_significance": item.cultural_significance,
            "traditional_technique": item.traditional_technique,
            "why_it_matters": item.why_it_matters,
            "preservation_status": item.preservation_status,
            "artisan": item.artisan,
            "status": item.status,
            "image_url": item.image_url,
            "audio_url": item.audio_url,
            "video_url": item.video_url,
            "tags": [t.strip() for t in item.tags.split(",")] if item.tags else [],
            "sources": item.sources,
            "embedding_id": item.embedding_id,
            "view_count": item.view_count,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }
        return cls(**data)
