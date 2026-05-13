import sqlite3
import random
from flask import Blueprint, render_template_string, request, redirect, url_for, session, jsonify
from flask_login import current_user

recc_bp = Blueprint("recc", __name__)
DB_PATH = "instance/database.db"

def get_all_stalls():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stall")
    rows = cursor.fetchall()
    conn.close()
    stalls = []
    for row in rows:
        stalls.append({
            "id": row["id"],
            "name": row["name"],
            "category": (row["category"] or "").lower(),
            "description": row["description"] or "No description available.",
        })
    return stalls

QUESTIONS = [
    {
        "id": "mood",
        "question": "What's your vibe today?",
        "emoji": "🤩",
        "options": {
            "a": {"label": "Feeling a little bit dangerous today 🌶️", "tags": {"category": "western"}},
            "b": {"label": "I feel so different today", "tags": {"category": "korean"}},
            "c": {"label": "I feel colorful today", "tags": {"category": "chinese"}},
            "d": {"label": "I feel so calm today", "tags": {"category": "malay"}},
        }
    },
    {
        "id": "budget",
        "question": "What does your budget look like?",
        "emoji": "💸",
        "options": {
            "a": {"label": "Broke student 💔 (under RM10)", "tags": {}},
            "b": {"label": "Moderate (RM10+)", "tags": {}},
            "c": {"label": "Treating myself today! (RM15+)", "tags": {}},
        }
    },
    {
        "id": "dietary",
        "question": "Any dietary preference?",
        "emoji": "👀",
        "options": {
            "a": {"label": "Halal only", "tags": {}},
            "b": {"label": "Vegetarian", "tags": {}},
            "c": {"label": "No preference", "tags": {}},
        }
    },
    {
        "id": "category",
        "question": "Feeling any particular cuisine?",
        "emoji": "🍔",
        "options": {
            "a": {"label": "Local / Malay", "tags": {"category": "malay"}},
            "b": {"label": "Western", "tags": {"category": "western"}},
            "c": {"label": "Mamak", "tags": {"category": "mamak"}},
            "d": {"label": "Arab", "tags": {"category": "arab"}},
            "e": {"label": "Japanese", "tags": {"category": "japanese"}},
            "f": {"label": "Korean", "tags": {"category": "korean"}},
            "g": {"label": "Chinese", "tags": {"category": "chinese"}},
            "h": {"label": "Anything!", "tags": {}},
        }
    },
    {
        "id": "hunger",
        "question": "How hungry are you right now?",
        "emoji": "🤤",
        "options": {
            "a": {"label": "Starving — give me a full meal", "tags": {}},
            "b": {"label": "Just a little snacky", "tags": {}},
        }
    },
]

def stall_score(stall, preferences):
    score = 0
    for key, value in preferences.items():
        stall_value = stall.get(key, "")
        if isinstance(stall_value, str) and isinstance(value, str):
            if stall_value.lower() == value.lower():
                score += 1
    return score

def get_recommendation(answers):
    stalls = get_all_stalls()
    preferences = {}
    for q in QUESTIONS:
        qid = q["id"]
        if qid in answers:
            selected = answers[qid]
            tags = q["options"].get(selected, {}).get("tags", {})
            preferences.update(tags)
    scored = [(stall, stall_score(stall, preferences)) for stall in stalls]
    if not scored:
        return random.choice(stalls), "random", preferences
    max_score = max(s for _, s in scored)
    if max_score == 0:
        result = random.choice(stalls)
        mode = "random"
    else:
        top_stalls = [stall for stall, s in scored if s == max_score]
        result = random.choice(top_stalls)
        mode = "matched"
    return result, mode, preferences

def generate_reason(stall, preferences):
    reasons = []
    cat = preferences.get("category", "")
    if cat:
        reasons.append(f"matches your {cat} cuisine craving")
    if not reasons:
        reasons.append("felt right for you today 🎲")
    return "We picked this because it " + ", and ".join(reasons) + "!"

def is_manager():
    try:
        return current_user.is_authenticated and current_user.role == "manager"
    except:
        return False

@recc_bp.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        answers = {}
        for q in QUESTIONS:
            answers[q["id"]] = request.form.get(q["id"], "")
        stall, mode, preferences = get_recommendation(answers)
        if not stall:
            return "No stalls available yet.", 404
        reason = generate_reason(stall, preferences)
        return render_template_string(RESULT_PAGE, stall=stall, reason=reason, mode=mode)
    return render_template_string(QUIZ_PAGE, questions=QUESTIONS)

@recc_bp.route("/quiz/api", methods=["POST"])
def quiz_api():
    data = request.get_json()
    answers = {q["id"]: data.get(q["id"], "") for q in QUESTIONS}
    stall, mode, preferences = get_recommendation(answers)
    if not stall:
        return jsonify({"error": "No stalls available"}), 404
    reason = generate_reason(stall, preferences)
    return jsonify({
    "id": stall["id"],
    "name": stall["name"],
    "category": stall["category"],
    "description": stall["description"],
    "reason": reason,
    "mode": mode
})

QUIZ_PAGE = """
<h2>🍴 What Should I Eat?</h2>
<form method="POST">
{% for q in questions %}
<p><b>{{ q.emoji }} {{ q.question }}</b></p>
{% for key, opt in q.options.items() %}
<input type="radio" name="{{ q.id }}" value="{{ key }}" required> {{ opt.label }}<br>
{% endfor %}<br>
{% endfor %}
<button type="submit">Find my food! 🍽️</button>
</form>
"""

RESULT_PAGE = """
<h2>🍴 We recommend: {{ stall.name }}</h2>
<p>📍 {{ stall.description }}</p>
<p>💬 {{ reason }}</p>
{% if mode == "random" %}<p>🎲 (Random pick — no strong preference detected)</p>{% endif %}
<br><a href="/quiz">Try again</a>
<br><a href="/rating/{{ stall.id }}">View stall & rate</a>
"""