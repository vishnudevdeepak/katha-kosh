"""
Utility helpers for Kathā-Kosh backend.
"""
import os
import re
import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

from app.config import settings


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


async def save_upload_file(upload_file: UploadFile, subfolder: str = "") -> str:
    """Save an uploaded file and return the relative path."""
    contents = await upload_file.read()

    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE // (1024 * 1024)}MB",
        )

    ext = Path(upload_file.filename).suffix if upload_file.filename else ".bin"
    filename = f"{uuid.uuid4().hex}{ext}"

    upload_dir = Path(settings.UPLOAD_DIR)
    if subfolder:
        upload_dir = upload_dir / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(contents)

    relative_path = f"/{settings.UPLOAD_DIR}/{subfolder}/{filename}" if subfolder else f"/{settings.UPLOAD_DIR}/{filename}"
    return relative_path


def parse_tags(tags_str: str) -> list:
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def tags_to_str(tags: list) -> str:
    return ",".join(tags)
