import sqlite3
import random
from flask import Blueprint, render_template_string, request, redirect, url_for, session

DB_PATH = "stalls.db"
recc_bp = Blueprint("recc", __name__)

def get_all_stalls():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stalls")
    rows = cursor.fetchall()
    conn.close()
    stalls = []
    for row in rows:
        stalls.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price_range": row["price_range"],
            "vibe": row["vibe"].split(","),
            "dietary": row["dietary"].split(","),
            "description": row["description"]
        })
    return stalls

QUESTIONS = [
    {"id": "hunger", "question": "How hungry are you right now?", "emoji": "🤤", "options": {"a": {"label": "Starving", "tags": {"vibe": "filling"}}, "b": {"label": "Not much", "tags": {"vibe": "light"}}}},
    {"id": "mood", "question": "What's your vibe today?", "emoji": "🤩", "options": {"a": {"label": "Feeling a little bit dangerous today", "tags": {"vibe": "explosive"}}, "b": {"label": "I feel so different today", "tags": {"vibe": "quirky"}}, "c": {"label": "I feel colorful today", "tags": {"vibe": "diversity"}}, "d": {"label": "I feel so calm today", "tags": {"vibe": "chill"}}}},
    {"id": "budget", "question": "What does your budget look like?", "emoji": "💸", "options": {"a": {"label": "Broke student 💔 (under RM10)", "tags": {"price_range": "cheap"}}, "b": {"label": "Moderate (RM10+)", "tags": {"price_range": "moderate"}}, "c": {"label": "Treating myself today! (RM15+)", "tags": {"price_range": "expensive"}}}},
    {"id": "dietary", "question": "Any dietary preference?", "emoji": "👀", "options": {"a": {"label": "Halal", "tags": {"dietary": "halal"}}, "b": {"label": "Vegetarian", "tags": {"dietary": "vegetarian"}}, "c": {"label": "No preference", "tags": {}}}},
    {"id": "category", "question": "Feeling any particular cuisine?", "emoji": "🍔", "options": {"a": {"label": "Local / Malay", "tags": {"category": "local"}}, "b": {"label": "Western", "tags": {"category": "western"}}, "c": {"label": "Mamak", "tags": {"category": "mamak"}}, "d": {"label": "Arab", "tags": {"category": "arab"}}, "e": {"label": "Japanese", "tags": {"category": "japanese"}}, "f": {"label": "Korean", "tags": {"category": "korean"}}, "g": {"label": "Chinese", "tags": {"category": "chinese"}}, "h": {"label": "Anything", "tags": {}}}},
]

def stall_score(stall, preferences):
    score = 0
    for key, value in preferences.items():
        stall_value = stall.get(key)
        if isinstance(value, list):
            if isinstance(stall_value, list):
                if any(v in stall_value for v in value):
                    score += 1
            else:
                if stall_value in value:
                    score += 1
        else:
            if isinstance(stall_value, list):
                if value in stall_value:
                    score += 1
            else:
                if stall_value == value:
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
    if preferences.get("price_range") == "cheap":
        reasons.append("fits your budget")
    elif preferences.get("price_range") == "expensive":
        reasons.append("because you deserve a treat today")
    if preferences.get("vibe") == "filling":
        reasons.append("will keep you full")
    elif preferences.get("vibe") == "quick":
        reasons.append("is quick to grab")
    elif preferences.get("vibe") == "explosive":
        reasons.append("matches your dangerous mood 🌶️")
    elif preferences.get("vibe") == "quirky":
        reasons.append("matches your unique taste")
    if preferences.get("dietary") == "halal":
        reasons.append("is halal-certified")
    if not reasons:
        reasons.append("felt right for you today 🎲")
    return "We picked this because it " + ", and ".join(reasons) + "!"

def is_admin():
    return session.get("role") == "admin"

@recc_bp.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        answers = {}
        for q in QUESTIONS:
            answers[q["id"]] = request.form.get(q["id"], "")
        stall, mode, preferences = get_recommendation(answers)
        reason = generate_reason(stall, preferences)
        return render_template_string(RESULT_PAGE, stall=stall, reason=reason, mode=mode)
    return render_template_string(QUIZ_PAGE, questions=QUESTIONS)

# ADD THIS to reccsystem.py after your existing /quiz route

from flask import jsonify

@recc_bp.route("/quiz/api", methods=["POST"])
def quiz_api():
    data = request.get_json()
    answers = {
        "hunger":   data.get("hunger", ""),
        "mood":     data.get("mood", ""),
        "budget":   data.get("budget", ""),
        "dietary":  data.get("dietary", ""),
        "category": data.get("category", ""),
    }
    stall, mode, preferences = get_recommendation(answers)
    reason = generate_reason(stall, preferences)

    return jsonify({
        "id":          stall["id"],
        "name":        stall["name"],
        "category":    stall["category"],
        "price_range": stall["price_range"],
        "description": stall["description"],
        "reason":      reason,
        "mode":        mode
    })

@recc_bp.route("/admin/stalls")
def admin_stalls():
    if not is_admin():
        return "Access denied. Admins only.", 403
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stalls")
    stalls = cursor.fetchall()
    conn.close()
    return render_template_string(ADMIN_LIST_PAGE, stalls=stalls)

@recc_bp.route("/admin/stalls/add", methods=["GET", "POST"])
def admin_add_stall():
    if not is_admin():
        return "Access denied. Admins only.", 403
    if request.method == "POST":
        name        = request.form["name"]
        category    = request.form["category"]
        price_range = request.form["price_range"]
        vibe        = request.form["vibe"]
        dietary     = request.form["dietary"]
        description = request.form["description"]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stalls (name, category, price_range, vibe, dietary, description) VALUES (?, ?, ?, ?, ?, ?)", (name, category, price_range, vibe, dietary, description))
        conn.commit()
        conn.close()
        return redirect(url_for("recc.admin_stalls"))
    return render_template_string(ADMIN_FORM_PAGE, stall=None, action="Add")

@recc_bp.route("/admin/stalls/edit/<int:stall_id>", methods=["GET", "POST"])
def admin_edit_stall(stall_id):
    if not is_admin():
        return "Access denied. Admins only.", 403
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if request.method == "POST":
        name        = request.form["name"]
        category    = request.form["category"]
        price_range = request.form["price_range"]
        vibe        = request.form["vibe"]
        dietary     = request.form["dietary"]
        description = request.form["description"]
        cursor.execute("UPDATE stalls SET name=?, category=?, price_range=?, vibe=?, dietary=?, description=? WHERE id=?", (name, category, price_range, vibe, dietary, description, stall_id))
        conn.commit()
        conn.close()
        return redirect(url_for("recc.admin_stalls"))
    cursor.execute("SELECT * FROM stalls WHERE id=?", (stall_id,))
    stall = cursor.fetchone()
    conn.close()
    return render_template_string(ADMIN_FORM_PAGE, stall=stall, action="Edit")

@recc_bp.route("/admin/stalls/delete/<int:stall_id>", methods=["POST"])
def admin_delete_stall(stall_id):
    if not is_admin():
        return "Access denied. Admins only.", 403
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stalls WHERE id=?", (stall_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("recc.admin_stalls"))

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
"""

ADMIN_LIST_PAGE = """
<h2>Admin — Manage Stalls</h2>
<a href="/admin/stalls/add">+ Add New Stall</a><br><br>
<table border="1" cellpadding="8">
<tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Vibe</th><th>Dietary</th><th>Actions</th></tr>
{% for stall in stalls %}
<tr>
<td>{{ stall.id }}</td><td>{{ stall.name }}</td><td>{{ stall.category }}</td>
<td>{{ stall.price_range }}</td><td>{{ stall.vibe }}</td><td>{{ stall.dietary }}</td>
<td>
<a href="/admin/stalls/edit/{{ stall.id }}">Edit</a> |
<form method="POST" action="/admin/stalls/delete/{{ stall.id }}" style="display:inline">
<button type="submit" onclick="return confirm('Delete this stall?')">Delete</button>
</form>
</td>
</tr>
{% endfor %}
</table>
"""

ADMIN_FORM_PAGE = """
<h2>{{ action }} Stall</h2>
<form method="POST">
Name: <input type="text" name="name" value="{{ stall.name if stall else '' }}" required><br><br>
Category: <input type="text" name="category" value="{{ stall.category if stall else '' }}" required><br><br>
Price Range:
<select name="price_range">
<option value="cheap" {{ 'selected' if stall and stall.price_range == 'cheap' }}>Cheap</option>
<option value="moderate" {{ 'selected' if stall and stall.price_range == 'moderate' }}>Moderate</option>
<option value="expensive" {{ 'selected' if stall and stall.price_range == 'expensive' }}>Expensive</option>
</select><br><br>
Vibe (comma-separated): <input type="text" name="vibe" value="{{ stall.vibe if stall else '' }}" required><br><br>
Dietary (comma-separated): <input type="text" name="dietary" value="{{ stall.dietary if stall else '' }}" required><br><br>
Description: <input type="text" name="description" value="{{ stall.description if stall else '' }}" required><br><br>
<button type="submit">{{ action }} Stall</button>
<a href="/admin/stalls">Cancel</a>
</form>
"""
