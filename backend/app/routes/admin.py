"""
Admin routes: stats, item management, status updates.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.heritage_item import HeritageItem
from app.models.contribution import Contribution
from app.models.user import User
from app.schemas.heritage_item import HeritageItemResponse, HeritageItemUpdate
from app.services import item_service

router = APIRouter(tags=["admin"])


def _to_response(item: HeritageItem) -> HeritageItemResponse:
    return HeritageItemResponse.from_orm_with_tags(item)


@router.get("/admin/stats")
def admin_stats(db: Session = Depends(get_db)):
    total_items = db.query(HeritageItem).count()
    published = db.query(HeritageItem).filter(HeritageItem.status == "published").count()
    pending = db.query(HeritageItem).filter(HeritageItem.status == "pending").count()
    rejected = db.query(HeritageItem).filter(HeritageItem.status == "rejected").count()
    total_contributions = db.query(Contribution).count()
    pending_contributions = db.query(Contribution).filter(Contribution.status == "pending").count()
    total_users = db.query(User).count()
    total_views = db.query(HeritageItem).with_entities(
        db.query(HeritageItem.view_count).subquery()
    )
    # Simpler view count sum
    from sqlalchemy import func as sqlfunc
    view_sum = db.query(sqlfunc.sum(HeritageItem.view_count)).scalar() or 0

    return {
        "items": {
            "total": total_items,
            "published": published,
            "pending": pending,
            "rejected": rejected,
        },
        "contributions": {
            "total": total_contributions,
            "pending": pending_contributions,
        },
        "users": {"total": total_users},
        "total_views": view_sum,
    }


@router.get("/admin/items", response_model=dict)
def admin_list_items(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(HeritageItem)
    if status_filter:
        query = query.filter(HeritageItem.status == status_filter)
    total = query.count()
    items = query.order_by(HeritageItem.created_at.desc()).offset(offset).limit(limit).all()
    return {
        "items": [_to_response(i) for i in items],
        "total": total,
    }


@router.put("/admin/items/{item_id}/status", response_model=HeritageItemResponse)
def update_item_status(
    item_id: int,
    new_status: str = Query(..., alias="status"),
    db: Session = Depends(get_db),
):
    if new_status not in ("published", "pending", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status value")
    item = db.query(HeritageItem).filter(HeritageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.status = new_status
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.put("/admin/items/{item_id}", response_model=HeritageItemResponse)
def admin_update_item(item_id: int, item_in: HeritageItemUpdate, db: Session = Depends(get_db)):
    item = db.query(HeritageItem).filter(HeritageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = item_service.update_item(db, item, item_in)
    return _to_response(item)
