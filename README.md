# Best Presenter

EQI 6축 프레젠테이션 평가 시스템 — 트랜스크립트를 입력하면 LLM이 자동 채점(100점 + 6축 레이더 차트)하고, 개선 포인트와 리라이트를 제공합니다.

## 목차

- [사전 요구사항](#사전-요구사항)
- [설치 (개발 환경)](#설치-개발-환경)
- [실행](#실행)
- [네이티브 앱 빌드](#네이티브-앱-빌드)
- [프로젝트 구조](#프로젝트-구조)
- [환경 변수](#환경-변수)

---

## 사전 요구사항

| 도구 | 버전 | 용도 |
|------|------|------|
| Node.js | 18+ | Electron, 프론트엔드 빌드 |
| Python | 3.10+ | FastAPI 백엔드 |
| pip | 최신 | Python 패키지 설치 |
| PyInstaller | 6+ | 네이티브 앱 빌드 시 필요 |

---

## 설치 (개발 환경)

### 1. 저장소 클론

```bash
git clone <repository-url>
cd best-presenter
```

### 2. Node 의존성 설치

```bash
npm install
```

> `postinstall` 스크립트가 자동으로 `frontend/`의 의존성도 설치합니다.

### 3. Python 의존성 설치

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 4. 환경 변수 설정

```bash
cp backend/.env.example backend/.env   # 또는 직접 생성
```

`backend/.env` 파일에 OpenAI API 키를 입력합니다:

```
OPENAI_API_KEY=sk-your-api-key-here
```

> 앱 실행 후 설정 모달에서도 API 키를 입력할 수 있습니다.

---

## 실행

### 개발 모드 (Electron + 시스템 Python)

```bash
# 프론트엔드 빌드 + Electron 실행
npm start

# 또는 프론트엔드가 이미 빌드되어 있다면
npm run dev
```

이 모드에서는 시스템 Python으로 FastAPI 백엔드(`uvicorn`)를 자동 실행합니다.

### 백엔드만 실행 (프론트엔드 개발 시)

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

프론트엔드 개발 서버:

```bash
cd frontend
npm run dev
```

`http://localhost:5173`에서 프론트엔드, `http://localhost:8000`에서 API를 사용합니다.

---

## 네이티브 앱 빌드

Python 설치 없이 동작하는 독립 실행 파일(.dmg / .exe)을 만듭니다.

### 빌드 사전 준비

```bash
# PyInstaller 설치 (빌드 머신에만 필요)
pip install pyinstaller
```

### macOS (.dmg)

```bash
npm run build:mac
```

### Windows (.exe)

```bash
npm run build:win
```

### 빌드 과정

`build:mac` / `build:win` 명령은 아래 3단계를 순서대로 실행합니다:

1. **프론트엔드 빌드** — `frontend/dist/` 생성
2. **PyInstaller 백엔드 번들** — `dist-backend/best-presenter-backend/` 생성 (frontend/dist 포함)
3. **electron-builder 패키징** — `dist/` 에 .dmg 또는 .exe 생성

### 빌드 결과물

```
dist/
├── Best Presenter-x.x.x.dmg      # macOS 설치 파일
├── Best Presenter Setup x.x.x.exe # Windows 설치 파일
```

### 설치 및 실행

- **macOS**: `.dmg`를 열고 `Best Presenter.app`을 Applications 폴더로 드래그
- **Windows**: `.exe` 설치 파일 실행 후 안내에 따라 설치

앱 실행 시 자동으로 백엔드 서버가 시작되며, 설정 모달에서 OpenAI API 키를 입력하면 바로 사용할 수 있습니다.

---

## 프로젝트 구조

```
best-presenter/
├── frontend/          # Vue.js 프론트엔드 (Vite)
├── backend/           # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py        # FastAPI 앱 진입점
│   │   ├── models/        # DB, 스키마
│   │   └── routes/        # API 라우트 (evaluate, history, settings)
│   ├── run.py             # PyInstaller 진입점
│   ├── best-presenter.spec # PyInstaller 빌드 스펙
│   ├── hooks/             # PyInstaller 커스텀 훅
│   └── requirements.txt
├── electron/          # Electron 메인 프로세스
│   ├── main.js
│   └── preload.js
├── package.json
└── README.md
```

---

## 환경 변수

| 변수 | 설명 | 필수 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | O (앱 내 설정 모달에서도 입력 가능) |

---

## 데이터 저장 위치

- **개발 모드**: `backend/evaluations.db`
- **패키징 앱**: `~/.best-presenter/evaluations.db`

---

## 문제 해결

### 백엔드가 시작되지 않음
- 개발 모드: Python 3.10+ 설치 여부와 가상환경 활성화를 확인하세요.
- 패키징 앱: 포트 8000이 다른 프로세스에 의해 사용 중인지 확인하세요.

### API 키 오류
- 설정 모달에서 유효한 OpenAI API 키를 입력했는지 확인하세요.

### 빌드 실패
- `node_modules/`와 `frontend/node_modules/`를 삭제 후 `npm install`을 다시 실행하세요.
- Python 가상환경에 `pyinstaller`와 `requirements.txt`의 모든 패키지가 설치되어 있는지 확인하세요.
