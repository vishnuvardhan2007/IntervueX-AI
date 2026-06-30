# IntervueX-AI

> A rule-based interview question generator for AI/ML roles. Enter your name, target company, and role — the engine maps your profile to the right topics, difficulty mix, and 8–12 tailored questions instantly. No LLM. No API. Pure Python rules.

---

## Features

- **Role-aware topic mapping** — 16+ role profiles (Gen AI Engineer, ML Engineer, Data Scientist, NLP Engineer, MLOps, etc.) each mapped to weighted topic categories
- **Experience-calibrated difficulty** — Fresher gets 50% easy questions; 5+ years gets 70% hard
- **114+ curated questions** — Spanning Gen AI, Machine Learning, Python, NLP, Deep Learning, System Design, Statistics, and Behavioral
- **Follow-up hints** — Every question includes an interviewer-style follow-up to deepen preparation
- **Rules transparency** — The UI shows exactly which rules fired for your profile
- **Print-ready** — Clean, formatted output you can print as PDF or study on screen
- **Zero API calls** — Fully deterministic, no LLM dependency, instant generation

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| Rules Engine | Pure Python (difflib fuzzy matching) |
| Question Bank | JSON (114 questions, 8 topics) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Fonts | Inter (Google Fonts) |

---

## Project Structure

```
IntervueX-AI/
├── app.py                  # Flask routes
├── requirements.txt
├── engine/
│   ├── rules.py            # Rules engine — role→topic mapping, difficulty distribution
│   ├── question_bank.py    # Question loader and filter
│   └── generator.py        # Orchestrates rules + bank → interview output
├── data/
│   └── questions.json      # 114-question bank (8 topics, 3 difficulties)
├── templates/
│   ├── index.html          # Landing page (hero, features, how-it-works, form)
│   └── interview.html      # Generated interview output page
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## How the Rules Engine Works

1. **Role normalization** — Your role title is lowercased and fuzzy-matched against 16 known role profiles using `difflib.SequenceMatcher`
2. **Topic weighting** — Each role profile defines topic weights (e.g. Gen AI Engineer → 40% Gen AI, 20% Python, 20% ML …)
3. **Difficulty distribution** — Experience level controls the easy/medium/hard ratio:

| Experience | Easy | Medium | Hard |
|---|---|---|---|
| Fresher | 50% | 40% | 10% |
| 0–1 Year | 35% | 45% | 20% |
| 1–3 Years | 20% | 50% | 30% |
| 3–5 Years | 10% | 40% | 50% |
| 5+ Years | 0% | 30% | 70% |

4. **Question selection** — Questions are drawn per topic per difficulty, with no duplicates and a guaranteed minimum of 1 per topic
5. **Behavioral rule** — Every interview always includes 1–2 behavioral questions regardless of role

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/vishnuvardhan2007/IntervueX-AI.git
cd IntervueX-AI

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Usage

1. Enter your **name**, **target company**, and **role** (e.g. "Gen AI Engineer", "ML Research Intern")
2. Select your **experience level**
3. Click **Generate My Interview**
4. Browse questions by topic, toggle follow-up hints, and print when ready

---

## Supported Roles

| Role | Primary Topics |
|---|---|
| Gen AI Engineer | Gen AI, Python, Machine Learning, System Design |
| LLM Engineer | Gen AI, NLP, Python, Machine Learning |
| ML Engineer | Machine Learning, Python, Deep Learning, System Design |
| Data Scientist | Machine Learning, Python, Statistics, NLP |
| NLP Engineer | NLP, Machine Learning, Python, Gen AI |
| Deep Learning Engineer | Deep Learning, Machine Learning, Python |
| Computer Vision Engineer | Deep Learning, Machine Learning, Python |
| MLOps Engineer | System Design, Machine Learning, Python |
| AI Research Intern | Gen AI, Machine Learning, Deep Learning, Python |
| Data Engineer | Python, System Design, Statistics |
| Software Engineer | Python, System Design, Machine Learning |

> Roles not in this list are fuzzy-matched to the closest profile.

---

## Built For

Gen AI Internship Project — demonstrating a deterministic, rule-based approach to interview generation without relying on any LLM or external API.

---

## License

MIT License — free to use, modify, and distribute.
