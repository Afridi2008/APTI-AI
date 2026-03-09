# Apti-AI — Aptitude Practice Web App

A full-stack web application for aptitude test preparation with AI-powered explanations.

## Tech Stack
- **Frontend** : HTML, CSS, JavaScript, Chart.js
- **Backend**  : Python (Flask)
- **Database** : MySQL
- **AI**       : OpenAI / Anthropic / Ollama (your choice)

---

## Quick Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up MySQL

```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure `config.py`

Edit these values:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",        # your MySQL username
    "password": "YOUR_PASS",   # your MySQL password
    "database": "aptitude_ai"
}

LLM_PROVIDER  = "openai"       # "openai" | "anthropic" | "ollama"
OPENAI_API_KEY = "sk-..."      # paste your API key
```

### 4. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Project Structure

```
apti-ai/
├── app.py              # Flask app — routes & logic
├── config.py           # DB + LLM credentials
├── requirements.txt
│
├── templates/
│   ├── index.html      # Landing page
│   ├── login.html      # Login + Signup
│   ├── dashboard.html  # Performance dashboard
│   └── quiz.html       # Quiz + Results page
│
├── static/
│   ├── css/style.css   # Global styles (dark theme)
│   └── js/quiz.js      # Timer, submission, AI explanation
│
├── database/
│   └── schema.sql      # Tables + 15 seed questions
│
└── llm/
    └── explain.py      # LLM integration (OpenAI/Anthropic/Ollama)
```

---

## Features (v1)

| Feature | Status |
|---|---|
| User signup / login | ✅ |
| Timed quiz (10 min) | ✅ |
| Topic-based filtering | ✅ |
| Submit & score | ✅ |
| AI step-by-step explanation | ✅ |
| Per-question result breakdown | ✅ |
| Topic-wise accuracy chart | ✅ |
| Recent quiz history | ✅ |

---

## Adding More Questions

Run SQL inserts against the `questions` table:

```sql
INSERT INTO questions (topic, question, option1, option2, option3, option4, answer)
VALUES ('Probability', 'Your question here?', 'A', 'B', 'C', 'D', 'option1');
```

`answer` must be one of: `option1`, `option2`, `option3`, `option4`.

---

## Switching LLM Provider

In `config.py`, set:

```python
LLM_PROVIDER = "anthropic"   # or "openai" or "ollama"
```

For local models (no API key needed):

```python
LLM_PROVIDER  = "ollama"
OLLAMA_MODEL  = "mistral"    # or llama3, gemma, etc.
```

Run Ollama with: `ollama run mistral`
