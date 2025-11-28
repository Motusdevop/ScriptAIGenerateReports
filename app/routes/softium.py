import base64
import binascii
import hashlib

from fastapi import APIRouter, HTTPException
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.services.softium_scraper import LessonScraper

router = APIRouter(prefix="/scraper", tags=["scraper"])


def decrypt_password(username: str, lesson_id: int, encrypted: str, iv_b64: str) -> str:
    """Расшифровывает пароль, отправленный с клиента."""
    try:
        key_material = f"{username}:{lesson_id}".encode("utf-8")
        key = hashlib.sha256(key_material).digest()
        iv = base64.b64decode(iv_b64)
        ciphertext = base64.b64decode(encrypted)
    except (ValueError, TypeError, binascii.Error) as exc:
        raise HTTPException(status_code=400, detail="Некорректные данные пароля") from exc

    try:
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(iv, ciphertext, None)
        return decrypted.decode("utf-8")
    except Exception as exc:  # pragma: no cover - защищаем расшифровку
        raise HTTPException(status_code=400, detail="Не удалось расшифровать пароль") from exc


@router.get("/get_lesson_data")
def scrape(username: str, password: str, lesson_id: int, password_iv: str | None = None):
    if password_iv:
        password = decrypt_password(username, lesson_id, password, password_iv)

    scraper = LessonScraper(username=username, password=password)

    data = scraper.get_lesson_data(lesson_id)
    return {"children": [c.to_dict() for c in data]}
