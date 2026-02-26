from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys

import aiosqlite

if getattr(sys, 'frozen', False):
    # PyInstaller bundle: store DB in user home directory (app bundle is read-only)
    _APP_DATA = Path.home() / ".best-presenter"
    _APP_DATA.mkdir(parents=True, exist_ok=True)
    DB_PATH = _APP_DATA / "evaluations.db"
else:
    DB_PATH = Path(__file__).parent.parent.parent / "evaluations.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                transcript TEXT NOT NULL,
                intent TEXT NOT NULL DEFAULT '',
                audience TEXT NOT NULL DEFAULT '',
                total_score INTEGER NOT NULL DEFAULT 0,
                result_json TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_evaluation(transcript: str, result: dict) -> str:
    eval_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()
    intent = result.get("meta", {}).get("intent", "")
    audience = result.get("meta", {}).get("audience", "")
    total_score = result.get("scores", {}).get("total", 0)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO evaluations (id, created_at, transcript, intent, audience, total_score, result_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (eval_id, now, transcript, intent, audience, total_score, json.dumps(result, ensure_ascii=False)),
        )
        await db.commit()

    return eval_id


async def get_evaluation(eval_id: str) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM evaluations WHERE id = ?", (eval_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "created_at": row["created_at"],
            "result": json.loads(row["result_json"]),
        }


async def save_multi_speaker_evaluation(transcript: str, result: dict) -> str:
    eval_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()
    speakers = result.get("speakers", [])
    # Use first speaker's evaluation for summary fields
    first_eval = {}
    evaluations = result.get("evaluations", {})
    if speakers and speakers[0] in evaluations:
        first_eval = evaluations[speakers[0]]
    intent = first_eval.get("meta", {}).get("intent", "")
    audience = first_eval.get("meta", {}).get("audience", "")
    total_score = first_eval.get("scores", {}).get("total", 0)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO evaluations (id, created_at, transcript, intent, audience, total_score, result_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (eval_id, now, transcript, intent, audience, total_score, json.dumps(result, ensure_ascii=False)),
        )
        await db.commit()

    return eval_id


async def list_evaluations(limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, created_at, intent, audience, total_score, transcript FROM evaluations ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "intent": row["intent"],
                "audience": row["audience"],
                "total_score": row["total_score"],
                "transcript_preview": row["transcript"][:100],
            }
            for row in rows
        ]
