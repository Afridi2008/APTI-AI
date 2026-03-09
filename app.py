from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from config import DB_CONFIG
from llm.explain import get_explanation
import hashlib

app = Flask(__name__)
app.secret_key = "apti_ai_secret_key_change_in_production"

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ─── AUTH ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name     = request.form["name"]
        email    = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                    (name, email, password))
        db.commit()
        user_id = cur.lastrowid
        session["user_id"] = user_id
        session["user_name"] = name
        return redirect(url_for("dashboard"))
    return render_template("login.html", mode="signup")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email    = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
        db = get_db(); cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        if user:
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        error = "Invalid email or password."
    return render_template("login.html", mode="login", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)

    # Topic-wise accuracy
    cur.execute("""
        SELECT ra.topic,
               COUNT(*) AS total,
               SUM(ra.is_correct) AS correct
        FROM result_answers ra
        JOIN results r ON ra.result_id = r.id
        WHERE r.user_id = %s
        GROUP BY ra.topic
    """, (session["user_id"],))
    topic_stats = cur.fetchall()

    cur.execute("""
        SELECT r.score, r.total_questions, r.date
        FROM results r
        WHERE r.user_id = %s
        ORDER BY r.date DESC LIMIT 5
    """, (session["user_id"],))
    recent = cur.fetchall()

    return render_template("dashboard.html",
                           name=session["user_name"],
                           topic_stats=topic_stats,
                           recent=recent)

# ─── QUIZ ─────────────────────────────────────────────────────────────────────

@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect(url_for("login"))
    topic = request.args.get("topic", "all")
    db = get_db(); cur = db.cursor(dictionary=True)
    if topic == "all":
        cur.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 10")
    else:
        cur.execute("SELECT * FROM questions WHERE topic=%s ORDER BY RAND() LIMIT 10", (topic,))
    questions = cur.fetchall()
    return render_template("quiz.html", questions=questions, topic=topic)

@app.route("/submit", methods=["POST"])
def submit():
    if "user_id" not in session:
        return redirect(url_for("login"))

    data      = request.get_json()
    answers   = data.get("answers", {})   # {q_id: chosen_option}
    db = get_db(); cur = db.cursor(dictionary=True)

    score = 0
    results_detail = []
    for q_id, user_ans in answers.items():
        cur.execute("SELECT * FROM questions WHERE id=%s", (q_id,))
        q = cur.fetchone()
        if not q:
            continue
        correct = q["answer"] == user_ans
        if correct:
            score += 1
        results_detail.append({
            "question": q["question"],
            "options": [q["option1"], q["option2"], q["option3"], q["option4"]],
            "user_answer": user_ans,
            "correct_answer": q["answer"],
            "is_correct": correct,
            "topic": q["topic"]
        })

    # Save result
    cur.execute("INSERT INTO results (user_id, score, total_questions) VALUES (%s,%s,%s)",
                (session["user_id"], score, len(answers)))
    db.commit()
    result_id = cur.lastrowid

    # Save per-answer breakdown
    for rd in results_detail:
        cur.execute("""INSERT INTO result_answers
                       (result_id, topic, is_correct) VALUES (%s,%s,%s)""",
                    (result_id, rd["topic"], rd["is_correct"]))
    db.commit()

    return jsonify({"score": score, "total": len(answers), "details": results_detail})

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    question       = data.get("question")
    correct_answer = data.get("correct_answer")
    explanation    = get_explanation(question, correct_answer)
    return jsonify({"explanation": explanation})

# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)