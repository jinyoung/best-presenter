from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


CONFIG_DIR = Path.home() / ".best-presenter"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    database_url: str = "sqlite+aiosqlite:///./evaluations.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def _load_json_config() -> dict:
    """Load config from ~/.best-presenter/config.json if it exists."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _build_settings() -> Settings:
    """Build Settings: .env first, then override with JSON config values."""
    s = Settings()
    cfg = _load_json_config()
    if cfg.get("openai_api_key"):
        s.openai_api_key = cfg["openai_api_key"]
    if cfg.get("openai_model"):
        s.openai_model = cfg["openai_model"]
    return s


settings = _build_settings()


def update_settings(*, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
    """Save settings to JSON config and update the runtime settings object."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cfg = _load_json_config()

    if api_key is not None:
        cfg["openai_api_key"] = api_key
        settings.openai_api_key = api_key
    if model is not None:
        cfg["openai_model"] = model
        settings.openai_model = model

    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
