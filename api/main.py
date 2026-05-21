from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI()

# Allow future frontend (Netlify) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we'll restrict this to your Netlify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "questions.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

@app.get("/subjects")
def get_subjects():
    subjects = sorted({q["subject"] for q in QUESTIONS})
    return subjects

@app.get("/topics")
def get_topics(subject: str | None = None):
    if subject:
        topics = sorted({q["topic"] for q in QUESTIONS if q["subject"] == subject})
    else:
        topics = sorted({q["topic"] for q in QUESTIONS})
    return topics

@app.get("/questions")
def get_questions(subject: str | None = None, topic: str | None = None):
    results = QUESTIONS
    if subject:
        results = [q for q in results if q["subject"] == subject]
    if topic:
        results = [q for q in results if q["topic"] == topic]
    return results