"""
Text Embedder — uses sentence-transformers if available,
falls back to deterministic hash-based pseudo-embeddings for demo.
"""


class TextEmbedder:
    def __init__(self):
        self._model = None
        self._available = False
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._available = True
            print("[TextEmbedder] sentence-transformers loaded successfully")
        except Exception as e:
            print(f"[TextEmbedder] sentence-transformers not available: {e}")
            print("[TextEmbedder] Using fallback hash-based embeddings for demo")

    @property
    def is_available(self) -> bool:
        return self._available

    def embed(self, text: str) -> list:
        if self._model:
            return self._model.encode(text).tolist()
        # Fallback: deterministic hash-based pseudo-embedding
        import hashlib
        import struct

        result = []
        seed = text.encode()
        for i in range(24):
            h = hashlib.md5(seed + i.to_bytes(4, "little")).digest()
            for j in range(0, 16, 4):
                val = struct.unpack("f", h[j : j + 4])[0]
                result.append(float(abs(val) % 1.0))
        return result[:384]

    def embed_batch(self, texts: list) -> list:
        if self._model:
            return [v.tolist() for v in self._model.encode(texts)]
        return [self.embed(t) for t in texts]
