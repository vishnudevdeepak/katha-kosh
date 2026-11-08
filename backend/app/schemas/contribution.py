from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ContributionCreate(BaseModel):
    title: str
    description: str
    type: str
    region: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    artisan: Optional[str] = None
    storyteller: Optional[str] = None
    contributor_name: str
    contributor_email: str
    contributor_role: Optional[str] = None
    sources: Optional[str] = None


class ContributionUpdate(BaseModel):
    status: Optional[str] = None
    review_notes: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    artisan: Optional[str] = None
    storyteller: Optional[str] = None


class ContributionResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    region: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    community: Optional[str] = None
    historical_period: Optional[str] = None
    artisan: Optional[str] = None
    storyteller: Optional[str] = None
    contributor_name: str
    contributor_email: str
    contributor_role: Optional[str] = None
    status: str
    review_notes: Optional[str] = None
    image_paths: Optional[str] = None
    sources: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
