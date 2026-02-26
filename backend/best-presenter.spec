# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Best Presenter backend (one-dir mode)."""

import os
import sys

block_cipher = None

# Path to frontend dist (built before PyInstaller runs)
frontend_dist = os.path.join('..', 'frontend', 'dist')

a = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        (frontend_dist, 'frontend_dist'),
    ],
    hiddenimports=[
        # uvicorn internals
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.http.httptools_impl',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.websockets.wsproto_impl',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.logging',
        # fastapi / starlette
        'fastapi',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'starlette.responses',
        'starlette.staticfiles',
        'starlette.routing',
        # pydantic (collected by hook but ensure core)
        'pydantic',
        'pydantic_settings',
        'pydantic_core',
        # aiosqlite
        'aiosqlite',
        # langchain / langgraph
        'langchain_core',
        'langchain_openai',
        'langgraph',
        # tiktoken
        'tiktoken',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        # openai / httpx
        'openai',
        'httpx',
        'httpcore',
        'h11',
        'anyio',
        'anyio._backends',
        'anyio._backends._asyncio',
        'sniffio',
        # dotenv
        'dotenv',
        # email-validator (often needed by pydantic)
        'email_validator',
        # multipart (starlette form parsing)
        'multipart',
        # app modules
        'app',
        'app.main',
        'app.models',
        'app.models.db',
        'app.routes',
        'app.routes.evaluate',
        'app.routes.history',
        'app.routes.settings',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'numpy.testing',
        'PIL',
        'pytest',
        # Heavy ML/data libs pulled in transitively but not needed
        'torch',
        'torchvision',
        'torchaudio',
        'lightning',
        'pytorch_lightning',
        'transformers',
        'datasets',
        'pandas',
        'sklearn',
        'scikit-learn',
        'statsmodels',
        'plotly',
        'numba',
        'llvmlite',
        'pyarrow',
        'openpyxl',
        'lxml',
        'IPython',
        'jupyter',
        'notebook',
        'nbformat',
        'nbconvert',
        'zmq',
        'jedi',
        'parso',
        'pygments',
        'boto3',
        'botocore',
        's3transfer',
        'psycopg2',
        'sqlalchemy',
        'lightgbm',
        'google.cloud',
        'google.api_core',
        'grpc',
        'grpcio',
        'tensorboard',
        'tensorflow',
        'keras',
        'cloudpickle',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='best-presenter-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for logging; Electron hides it
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='best-presenter-backend',
)
