import os
import json
import pdfplumber

PDF_DIR = "pdfs"
OUTPUT_FILE = "output/questions.json"

SUBJECT = "Mathematics"
TOPIC = "Algebra"

def extract_text_from_pdf(path):
    all_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            all_text += "\n" + text
    return all_text

def split_into_questions(text):
    # Very naive splitter: improve later for your own layout
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    questions = []
    current = []
    for ln in lines:
        if ln.lower().startswith(("q1", "q2", "q3", "question", "1.", "2.", "3.")):
            if current:
                questions.append(" ".join(current).strip())
                current = []
        current.append(ln)
    if current:
        questions.append(" ".join(current).strip())
    return questions

def build_question_objects(questions, subject, topic):
    objs = []
    for i, q in enumerate(questions, start=1):
        objs.append({
            "id": f"{subject.lower()}_{topic.lower()}_{i}",
            "subject": subject,
            "topic": topic,
            "text": q,
            "difficulty": "unknown",
            "marks": 1
        })
    return objs

def main():
    all_questions = []
    for fname in os.listdir(PDF_DIR):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(PDF_DIR, fname)
        text = extract_text_from_pdf(path)
        qs = split_into_questions(text)
        objs = build_question_objects(qs, SUBJECT, TOPIC)
        all_questions.extend(objs)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_questions)} questions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()