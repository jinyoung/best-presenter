import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.models.db import init_db
from app.routes.evaluate import router as evaluate_router
from app.routes.history import router as history_router
from app.routes.settings import router as settings_router

app = FastAPI(title="Best Presenter API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(settings_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await init_db()


# --- Static file serving for packaged (Electron) mode ---
if getattr(sys, 'frozen', False):
    # PyInstaller bundle: frontend_dist is embedded via spec datas
    _FRONTEND_DIST = Path(sys._MEIPASS) / "frontend_dist"
else:
    # Development: resolve relative to source tree
    _FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if _FRONTEND_DIST.is_dir():
    # Serve static assets (js, css, images) under /assets
    app.mount("/assets", StaticFiles(directory=str(_FRONTEND_DIST / "assets")), name="static-assets")

    # SPA fallback: any non-API GET request returns index.html
    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        file_path = _FRONTEND_DIST / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(_FRONTEND_DIST / "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Best Presenter API is running (frontend/dist not found — run frontend build first)"}
