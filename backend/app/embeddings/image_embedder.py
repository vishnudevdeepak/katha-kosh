"""
Image Embedder — uses CLIP (via transformers) if available,
falls back to deterministic hash-based pseudo-embeddings for demo.
"""


class ImageEmbedder:
    def __init__(self):
        self._model = None
        self._processor = None
        self._available = False
        try:
            from transformers import CLIPProcessor, CLIPModel
            import torch  # noqa: F401

            self._model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self._processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self._available = True
            print("[ImageEmbedder] CLIP model loaded successfully")
        except Exception as e:
            print(f"[ImageEmbedder] CLIP not available: {e}")
            print("[ImageEmbedder] Using fallback hash-based embeddings for demo")

    @property
    def is_available(self) -> bool:
        return self._available

    def embed_image(self, image_bytes: bytes) -> list:
        if self._model and self._processor:
            from PIL import Image
            import io
            import torch

            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            inputs = self._processor(images=image, return_tensors="pt")
            with torch.no_grad():
                features = self._model.get_image_features(**inputs)
            return features[0].tolist()
        # Fallback: deterministic hash-based pseudo-embedding
        import hashlib
        import struct

        result = []
        for i in range(32):
            seed = image_bytes[:64] + i.to_bytes(4, "little")
            h = hashlib.md5(seed).digest()
            for j in range(0, 16, 4):
                val = struct.unpack("f", h[j : j + 4])[0]
                result.append(float(abs(val) % 1.0))
        return result[:512]
