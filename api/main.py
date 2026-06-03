from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",                 # dev
    "https://exams-banks1.netlify.app",      # your Netlify site
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Paths ---
# BASE_DIR: repo root (.. from api/)
BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_PATH = BASE_DIR / "api" / "questions.json"
PAGE_IMAGES_DIR = BASE_DIR / "extractor" / "output" / "page_images"

# --- Static media mount ---
if PAGE_IMAGES_DIR.exists():
    app.mount("/media", StaticFiles(directory=str(PAGE_IMAGES_DIR)), name="media")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Exam bank API running"}


@app.get("/questions")
def get_questions(request: Request):
    """
    Return all questions from questions.json.
    Each question may include a 'media' array.
    For image-like media ('image' or 'page_image'), attach a full URL.
    """
    base_url = str(request.base_url).rstrip("/")

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    for q in questions:
        media_list = q.get("media", [])
        for m in media_list:
            m_type = m.get("type")
            fname = m.get("file")
            if m_type in ("image", "page_image") and fname:
                m["url"] = f"{base_url}/media/{fname}"

    return questions