from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings, update_settings

router = APIRouter()


class SettingsResponse(BaseModel):
    api_key_set: bool
    api_key_masked: str
    model: str


class SettingsUpdate(BaseModel):
    api_key: Optional[str] = None
    model: Optional[str] = None


def _mask_key(key: str) -> str:
    if not key or len(key) < 8:
        return ""
    return key[:3] + "..." + key[-4:]


@router.get("/settings", response_model=SettingsResponse)
async def get_settings():
    return SettingsResponse(
        api_key_set=bool(settings.openai_api_key),
        api_key_masked=_mask_key(settings.openai_api_key),
        model=settings.openai_model,
    )


@router.post("/settings", response_model=SettingsResponse)
async def save_settings(body: SettingsUpdate):
    update_settings(api_key=body.api_key, model=body.model)
    return SettingsResponse(
        api_key_set=bool(settings.openai_api_key),
        api_key_masked=_mask_key(settings.openai_api_key),
        model=settings.openai_model,
    )
