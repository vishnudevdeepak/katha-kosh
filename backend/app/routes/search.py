"""
Search routes: text search, image search, autocomplete suggestions.
"""
from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.search import TextSearchRequest, SearchResponse, SuggestionResponse
from app.services.search_service import search_service
from app.models.heritage_item import HeritageItem

router = APIRouter(tags=["search"])


@router.post("/search/text", response_model=SearchResponse)
def text_search(request: TextSearchRequest, db: Session = Depends(get_db)):
    results = search_service.search_text(
        query=request.query,
        db=db,
        limit=request.limit,
        filters=request.filters,
    )
    return SearchResponse(
        results=results,
        total=len(results),
        query=request.query,
    )


@router.post("/search/image", response_model=SearchResponse)
async def image_search(
    image: UploadFile = File(...),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")
    results = search_service.search_image(image_bytes=image_bytes, db=db, limit=limit)
    return SearchResponse(
        results=results,
        total=len(results),
        query=f"image:{image.filename}",
    )


@router.get("/search/suggestions", response_model=SuggestionResponse)
def search_suggestions(
    q: str = Query(..., min_length=1),
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db),
):
    like = f"%{q}%"
    items = (
        db.query(HeritageItem.title)
        .filter(HeritageItem.status == "published", HeritageItem.title.ilike(like))
        .limit(limit)
        .all()
    )
    suggestions = [row[0] for row in items]

    # Also add tag matches
    if len(suggestions) < limit:
        tag_items = (
            db.query(HeritageItem.tags)
            .filter(HeritageItem.status == "published", HeritageItem.tags.ilike(like))
            .limit(limit - len(suggestions))
            .all()
        )
        for row in tag_items:
            if row[0]:
                for tag in row[0].split(","):
                    tag = tag.strip()
                    if q.lower() in tag.lower() and tag not in suggestions:
                        suggestions.append(tag)

    return SuggestionResponse(suggestions=suggestions[:limit], query=q)
