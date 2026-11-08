"""
Heritage items routes.
"""
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.heritage_item import HeritageItem
from app.schemas.heritage_item import (
    HeritageItemCreate,
    HeritageItemUpdate,
    HeritageItemResponse,
)
from app.services import item_service
from app.services.search_service import search_service

router = APIRouter(tags=["items"])


def _to_response(item: HeritageItem) -> HeritageItemResponse:
    return HeritageItemResponse.from_orm_with_tags(item)


@router.get("/items", response_model=dict)
def list_items(
    type: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = item_service.get_items(
        db,
        type=type,
        region=region,
        state=state,
        language=language,
        search=search,
        status="published",
        limit=limit,
        offset=offset,
    )
    return {
        "items": [_to_response(i) for i in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/items/{item_id}", response_model=HeritageItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(HeritageItem).filter(
        HeritageItem.id == item_id,
        HeritageItem.status == "published",
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    # Increment view count
    item.view_count = (item.view_count or 0) + 1
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.get("/items/slug/{slug}", response_model=HeritageItemResponse)
def get_item_by_slug(slug: str, db: Session = Depends(get_db)):
    item = db.query(HeritageItem).filter(
        HeritageItem.slug == slug,
        HeritageItem.status == "published",
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item.view_count = (item.view_count or 0) + 1
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.post("/items", response_model=HeritageItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_in: HeritageItemCreate, db: Session = Depends(get_db)):
    item = item_service.create_item(db, item_in)
    # Index in vector store asynchronously
    try:
        search_service.index_item(item)
    except Exception as e:
        print(f"[items] Vector indexing failed (non-fatal): {e}")
    return _to_response(item)


@router.put("/items/{item_id}", response_model=HeritageItemResponse)
def update_item(item_id: int, item_in: HeritageItemUpdate, db: Session = Depends(get_db)):
    item = db.query(HeritageItem).filter(HeritageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item = item_service.update_item(db, item, item_in)
    return _to_response(item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(HeritageItem).filter(HeritageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)
    db.commit()
    return None


@router.get("/recommendations/{item_id}", response_model=List[HeritageItemResponse])
def get_recommendations(item_id: int, limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    recs = search_service.get_recommendations(item_id, db, limit=limit)
    return [_to_response(r) for r in recs]
