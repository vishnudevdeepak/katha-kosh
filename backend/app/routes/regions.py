"""
Regions and categories routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.heritage_item import HeritageItem

router = APIRouter(tags=["regions"])

HERITAGE_TYPES = [
    "folk_story",
    "craft",
    "folk_art",
    "textile",
    "pottery",
    "woodwork",
    "metalwork",
    "dance",
    "music",
    "ritual",
    "oral_history",
]


@router.get("/regions")
def list_regions(db: Session = Depends(get_db)):
    rows = (
        db.query(HeritageItem.state, func.count(HeritageItem.id).label("count"))
        .filter(HeritageItem.status == "published")
        .group_by(HeritageItem.state)
        .order_by(func.count(HeritageItem.id).desc())
        .all()
    )
    return {
        "regions": [{"name": row[0], "count": row[1]} for row in rows]
    }


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = (
        db.query(HeritageItem.type, func.count(HeritageItem.id).label("count"))
        .filter(HeritageItem.status == "published")
        .group_by(HeritageItem.type)
        .order_by(func.count(HeritageItem.id).desc())
        .all()
    )
    all_types = {t: 0 for t in HERITAGE_TYPES}
    for row in rows:
        all_types[row[0]] = row[1]

    return {
        "categories": [
            {"type": k, "label": k.replace("_", " ").title(), "count": v}
            for k, v in all_types.items()
        ]
    }
