"""
FAISS-based vector store for semantic search.
Falls back gracefully if FAISS is not installed.
"""
import os
import json


class VectorStore:
    def __init__(self, dimension: int = 384, index_path: str = "vector_index.faiss"):
        self._index = None
        self._id_map: list = []  # list of item IDs parallel to faiss index
        self._dimension = dimension
        self._index_path = index_path
        self._available = False
        self._faiss = None
        self._np = None

        try:
            import faiss
            import numpy as np

            self._faiss = faiss
            self._np = np
            self._index = faiss.IndexFlatL2(dimension)
            self._available = True
            print(f"[VectorStore] FAISS loaded. Dimension={dimension}")
            self._load_if_exists()
        except Exception as e:
            print(f"[VectorStore] FAISS not available: {e}")
            print("[VectorStore] Vector search disabled; SQL fallback will be used.")

    @property
    def is_available(self) -> bool:
        return self._available

    @property
    def total_vectors(self) -> int:
        if self._available and self._index is not None:
            return self._index.ntotal
        return 0

    def add(self, item_id: int, vector: list):
        if not self._available:
            return
        vec = self._np.array([vector], dtype="float32")
        self._index.add(vec)
        self._id_map.append(item_id)
        self._save()

    def remove(self, item_id: int):
        """Remove not supported by IndexFlatL2 directly; rebuild is needed."""
        if not self._available:
            return
        if item_id not in self._id_map:
            return
        # Rebuild index without this id
        idx_to_remove = self._id_map.index(item_id)
        all_vectors = self._np.zeros((len(self._id_map), self._dimension), dtype="float32")
        self._index.reconstruct_n(0, len(self._id_map), all_vectors)
        new_id_map = []
        new_vectors = []
        for i, mid in enumerate(self._id_map):
            if mid != item_id:
                new_id_map.append(mid)
                new_vectors.append(all_vectors[i])
        self._index = self._faiss.IndexFlatL2(self._dimension)
        if new_vectors:
            self._index.add(self._np.array(new_vectors, dtype="float32"))
        self._id_map = new_id_map
        self._save()

    def search(self, vector: list, k: int = 10) -> list:
        """Returns list of (item_id, distance) tuples sorted by distance ascending."""
        if not self._available or self._index is None or self._index.ntotal == 0:
            return []
        vec = self._np.array([vector], dtype="float32")
        k = min(k, self._index.ntotal)
        distances, indices = self._index.search(vec, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self._id_map):
                results.append((self._id_map[idx], float(dist)))
        return results

    def _save(self):
        try:
            self._faiss.write_index(self._index, self._index_path)
            with open(self._index_path + ".ids", "w") as f:
                json.dump(self._id_map, f)
        except Exception as e:
            print(f"[VectorStore] Save failed: {e}")

    def _load_if_exists(self):
        if os.path.exists(self._index_path):
            try:
                self._index = self._faiss.read_index(self._index_path)
                ids_path = self._index_path + ".ids"
                if os.path.exists(ids_path):
                    with open(ids_path) as f:
                        self._id_map = json.load(f)
                print(f"[VectorStore] Loaded existing index with {self._index.ntotal} vectors.")
            except Exception as e:
                print(f"[VectorStore] Could not load existing index: {e}")
