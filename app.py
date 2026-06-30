from flask import Flask, render_template, request
from engine.generator import InterviewGenerator
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

generator = InterviewGenerator()

EXPERIENCE_OPTIONS = [
    ("fresher", "Fresher / No Experience"),
    ("0-1",     "0–1 Year"),
    ("1-3",     "1–3 Years"),
    ("3-5",     "3–5 Years"),
    ("5+",      "5+ Years"),
]


@app.route("/")
def index():
    return render_template("index.html", experience_options=EXPERIENCE_OPTIONS)


@app.route("/generate", methods=["POST"])
def generate():
    name       = request.form.get("name", "").strip()
    company    = request.form.get("company", "").strip()
    role       = request.form.get("role", "").strip()
    experience = request.form.get("experience", "fresher")

    errors = []
    if not name:
        errors.append("Please enter your name.")
    if not company:
        errors.append("Please enter the company name.")
    if not role:
        errors.append("Please enter the role.")

    if errors:
        return render_template("index.html", experience_options=EXPERIENCE_OPTIONS, errors=errors,
                               prev={"name": name, "company": company, "role": role, "experience": experience})

    interview = generator.generate(name=name, company=company, role=role, experience=experience)
    return render_template("interview.html", interview=interview)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
