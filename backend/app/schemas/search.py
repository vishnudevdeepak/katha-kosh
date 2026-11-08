from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.schemas.heritage_item import HeritageItemResponse


class TextSearchRequest(BaseModel):
    query: str
    limit: int = 10
    filters: Optional[Dict[str, Any]] = None


class ImageSearchRequest(BaseModel):
    limit: int = 10


class SearchResult(BaseModel):
    item: HeritageItemResponse
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str


class SuggestionResponse(BaseModel):
    suggestions: List[str]
    query: str
