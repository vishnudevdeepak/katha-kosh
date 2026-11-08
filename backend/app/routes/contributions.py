"""
Contributions routes: submit, list, approve, reject.
"""
import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contribution import Contribution
from app.schemas.contribution import ContributionResponse, ContributionUpdate
from app.utils.helpers import save_upload_file

router = APIRouter(tags=["contributions"])


@router.get("/contributions", response_model=dict)
def list_contributions(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Contribution)
    if status_filter:
        query = query.filter(Contribution.status == status_filter)
    total = query.count()
    items = query.order_by(Contribution.created_at.desc()).offset(offset).limit(limit).all()
    return {
        "contributions": [ContributionResponse.model_validate(c) for c in items],
        "total": total,
    }


@router.post("/contributions", response_model=ContributionResponse, status_code=status.HTTP_201_CREATED)
async def submit_contribution(
    title: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    region: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    community: Optional[str] = Form(None),
    historical_period: Optional[str] = Form(None),
    artisan: Optional[str] = Form(None),
    storyteller: Optional[str] = Form(None),
    contributor_name: str = Form(...),
    contributor_email: str = Form(...),
    contributor_role: Optional[str] = Form(None),
    sources: Optional[str] = Form(None),
    images: Optional[list[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    image_paths = []
    if images:
        for image in images:
            if image.filename:
                try:
                    path = await save_upload_file(image, subfolder="contributions")
                    image_paths.append(path)
                except HTTPException:
                    raise
                except Exception as e:
                    print(f"[contributions] Image save failed: {e}")

    contribution = Contribution(
        title=title,
        description=description,
        type=type,
        region=region,
        state=state,
        district=district,
        language=language,
        community=community,
        historical_period=historical_period,
        artisan=artisan,
        storyteller=storyteller,
        contributor_name=contributor_name,
        contributor_email=contributor_email,
        contributor_role=contributor_role,
        sources=sources,
        status="pending",
        image_paths=json.dumps(image_paths) if image_paths else None,
    )
    db.add(contribution)
    db.commit()
    db.refresh(contribution)
    return ContributionResponse.model_validate(contribution)


@router.get("/contributions/{contribution_id}", response_model=ContributionResponse)
def get_contribution(contribution_id: int, db: Session = Depends(get_db)):
    c = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contribution not found")
    return ContributionResponse.model_validate(c)


@router.post("/contributions/{contribution_id}/approve", response_model=ContributionResponse)
def approve_contribution(contribution_id: int, review_notes: Optional[str] = None, db: Session = Depends(get_db)):
    c = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contribution not found")
    c.status = "approved"
    if review_notes:
        c.review_notes = review_notes
    db.commit()
    db.refresh(c)
    return ContributionResponse.model_validate(c)


@router.post("/contributions/{contribution_id}/reject", response_model=ContributionResponse)
def reject_contribution(contribution_id: int, review_notes: Optional[str] = None, db: Session = Depends(get_db)):
    c = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contribution not found")
    c.status = "rejected"
    if review_notes:
        c.review_notes = review_notes
    db.commit()
    db.refresh(c)
    return ContributionResponse.model_validate(c)
