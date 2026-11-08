"""
Item service: CRUD helpers and slug generation.
"""
import re
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.heritage_item import HeritageItem
from app.schemas.heritage_item import HeritageItemCreate, HeritageItemUpdate


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def _make_unique_slug(db: Session, base_slug: str, exclude_id: Optional[int] = None) -> str:
    slug = base_slug
    counter = 1
    while True:
        query = db.query(HeritageItem).filter(HeritageItem.slug == slug)
        if exclude_id:
            query = query.filter(HeritageItem.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


def create_item(db: Session, item_in: HeritageItemCreate) -> HeritageItem:
    base_slug = item_in.slug if item_in.slug else _slugify(item_in.title)
    slug = _make_unique_slug(db, base_slug)
    item = HeritageItem(
        title=item_in.title,
        slug=slug,
        description=item_in.description,
        type=item_in.type,
        region=item_in.region,
        state=item_in.state,
        district=item_in.district,
        language=item_in.language,
        community=item_in.community,
        historical_period=item_in.historical_period,
        cultural_significance=item_in.cultural_significance,
        traditional_technique=item_in.traditional_technique,
        why_it_matters=item_in.why_it_matters,
        preservation_status=item_in.preservation_status,
        artisan=item_in.artisan,
        status=item_in.status,
        image_url=item_in.image_url,
        audio_url=item_in.audio_url,
        video_url=item_in.video_url,
        tags=item_in.tags,
        sources=item_in.sources,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item: HeritageItem, item_in: HeritageItemUpdate) -> HeritageItem:
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def get_items(
    db: Session,
    type: Optional[str] = None,
    region: Optional[str] = None,
    state: Optional[str] = None,
    language: Optional[str] = None,
    search: Optional[str] = None,
    status: str = "published",
    limit: int = 20,
    offset: int = 0,
) -> (List[HeritageItem], int):
    query = db.query(HeritageItem)
    if status:
        query = query.filter(HeritageItem.status == status)
    if type:
        query = query.filter(HeritageItem.type == type)
    if region:
        query = query.filter(HeritageItem.region.ilike(f"%{region}%"))
    if state:
        query = query.filter(HeritageItem.state.ilike(f"%{state}%"))
    if language:
        query = query.filter(HeritageItem.language.ilike(f"%{language}%"))
    if search:
        like = f"%{search}%"
        from sqlalchemy import or_
        query = query.filter(
            or_(
                HeritageItem.title.ilike(like),
                HeritageItem.description.ilike(like),
                HeritageItem.tags.ilike(like),
                HeritageItem.community.ilike(like),
            )
        )
    total = query.count()
    items = query.order_by(HeritageItem.created_at.desc()).offset(offset).limit(limit).all()
    return items, total
