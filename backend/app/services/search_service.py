"""
Search service: combines text_embedder + vector_store for unified semantic search.
Falls back to SQL LIKE search if vector search is unavailable.
"""
from typing import Optional, List, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.embeddings.text_embedder import TextEmbedder
from app.embeddings.image_embedder import ImageEmbedder
from app.vector_store.faiss_store import VectorStore
from app.models.heritage_item import HeritageItem
from app.schemas.heritage_item import HeritageItemResponse
from app.schemas.search import SearchResult

# Module-level singletons (lazy-initialized)
_text_embedder: Optional[TextEmbedder] = None
_image_embedder: Optional[ImageEmbedder] = None
_vector_store: Optional[VectorStore] = None


def get_text_embedder() -> TextEmbedder:
    global _text_embedder
    if _text_embedder is None:
        _text_embedder = TextEmbedder()
    return _text_embedder


def get_image_embedder() -> ImageEmbedder:
    global _image_embedder
    if _image_embedder is None:
        _image_embedder = ImageEmbedder()
    return _image_embedder


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(dimension=384)
    return _vector_store


class SearchService:
    def search_text(
        self,
        query: str,
        db: Session,
        limit: int = 10,
        filters: Optional[dict] = None,
    ) -> List[SearchResult]:
        embedder = get_text_embedder()
        store = get_vector_store()

        db_query = db.query(HeritageItem).filter(HeritageItem.status == "published")
        if filters:
            if filters.get("type"):
                db_query = db_query.filter(HeritageItem.type == filters["type"])
            if filters.get("state"):
                db_query = db_query.filter(HeritageItem.state.ilike(f"%{filters['state']}%"))
            if filters.get("region"):
                db_query = db_query.filter(HeritageItem.region.ilike(f"%{filters['region']}%"))
            if filters.get("language"):
                db_query = db_query.filter(HeritageItem.language.ilike(f"%{filters['language']}%"))

        results: List[SearchResult] = []

        if store.is_available and store.total_vectors > 0:
            vector = embedder.embed(query)
            hits = store.search(vector, k=limit * 2)
            hit_ids = [item_id for item_id, _ in hits]
            dist_map = {item_id: dist for item_id, dist in hits}

            items = db_query.filter(HeritageItem.id.in_(hit_ids)).all()
            item_map = {item.id: item for item in items}

            for item_id, dist in hits:
                if item_id in item_map:
                    score = max(0.0, 1.0 - dist / 100.0)
                    results.append(
                        SearchResult(
                            item=HeritageItemResponse.from_orm_with_tags(item_map[item_id]),
                            score=round(score, 4),
                        )
                    )
                if len(results) >= limit:
                    break
        else:
            # SQL LIKE fallback
            like = f"%{query}%"
            items = (
                db_query.filter(
                    or_(
                        HeritageItem.title.ilike(like),
                        HeritageItem.description.ilike(like),
                        HeritageItem.tags.ilike(like),
                        HeritageItem.community.ilike(like),
                        HeritageItem.cultural_significance.ilike(like),
                    )
                )
                .limit(limit)
                .all()
            )
            for item in items:
                results.append(
                    SearchResult(
                        item=HeritageItemResponse.from_orm_with_tags(item),
                        score=1.0,
                    )
                )

        return results

    def search_image(
        self,
        image_bytes: bytes,
        db: Session,
        limit: int = 10,
    ) -> List[SearchResult]:
        embedder = get_image_embedder()
        store = get_vector_store()

        results: List[SearchResult] = []

        if store.is_available and store.total_vectors > 0:
            vector = embedder.embed_image(image_bytes)
            # Pad/trim to match text embedding dimension if needed
            dim = store._dimension
            if len(vector) > dim:
                vector = vector[:dim]
            elif len(vector) < dim:
                vector = vector + [0.0] * (dim - len(vector))

            hits = store.search(vector, k=limit)
            hit_ids = [item_id for item_id, _ in hits]
            dist_map = {item_id: dist for item_id, dist in hits}

            items = (
                db.query(HeritageItem)
                .filter(HeritageItem.id.in_(hit_ids), HeritageItem.status == "published")
                .all()
            )
            item_map = {item.id: item for item in items}

            for item_id, dist in hits:
                if item_id in item_map:
                    score = max(0.0, 1.0 - dist / 100.0)
                    results.append(
                        SearchResult(
                            item=HeritageItemResponse.from_orm_with_tags(item_map[item_id]),
                            score=round(score, 4),
                        )
                    )
        else:
            # Fallback: return most recent items
            items = (
                db.query(HeritageItem)
                .filter(HeritageItem.status == "published")
                .order_by(HeritageItem.view_count.desc())
                .limit(limit)
                .all()
            )
            for item in items:
                results.append(
                    SearchResult(
                        item=HeritageItemResponse.from_orm_with_tags(item),
                        score=0.5,
                    )
                )

        return results

    def get_recommendations(
        self,
        item_id: int,
        db: Session,
        limit: int = 5,
    ) -> List[HeritageItem]:
        item = db.query(HeritageItem).filter(HeritageItem.id == item_id).first()
        if not item:
            return []

        store = get_vector_store()
        embedder = get_text_embedder()

        if store.is_available and store.total_vectors > 0:
            text = f"{item.title} {item.description} {item.tags or ''} {item.type} {item.region}"
            vector = embedder.embed(text)
            hits = store.search(vector, k=limit + 2)
            rec_ids = [iid for iid, _ in hits if iid != item_id][:limit]
            if rec_ids:
                recs = db.query(HeritageItem).filter(
                    HeritageItem.id.in_(rec_ids),
                    HeritageItem.status == "published",
                ).all()
                return recs

        # SQL fallback: same region or type
        recs = (
            db.query(HeritageItem)
            .filter(
                HeritageItem.id != item_id,
                HeritageItem.status == "published",
                or_(
                    HeritageItem.region == item.region,
                    HeritageItem.type == item.type,
                ),
            )
            .order_by(HeritageItem.view_count.desc())
            .limit(limit)
            .all()
        )
        return recs

    def index_item(self, item: HeritageItem):
        """Add item to vector store after creation/update."""
        store = get_vector_store()
        if not store.is_available:
            return
        embedder = get_text_embedder()
        text = f"{item.title} {item.description or ''} {item.tags or ''} {item.type} {item.region} {item.cultural_significance or ''}"
        vector = embedder.embed(text)
        store.add(item.id, vector)


search_service = SearchService()
