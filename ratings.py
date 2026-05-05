import sqlite3
from flask import Blueprint, render_template_string, request, redirect, url_for, session

ratings_bp = Blueprint("ratings", __name__)
DB_PATH = "stalls.db"

TEMP_USER_ID = 3
TEMP_IS_ADMIN = False

def get_current_user_id():
    return session.get("user_id", TEMP_USER_ID) 

def is_logged_in():
    return True  

# def get_current_user_id():
#    return session.get("user_id")  

#def is_logged_in():
#    return "user_id" in session  

def is_admin():
    return TEMP_IS_ADMIN

def get_current_username():
    user_id = get_current_user_id()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "User"


def get_average_rating(stall_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating) FROM ratings WHERE stall_id=?", (stall_id,))
    avg = cursor.fetchone()[0]
    conn.close()
    return round(avg, 1) if avg else None

def user_already_rated(stall_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ratings WHERE stall_id=? AND user_id=?", (stall_id, user_id))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def user_already_reviewed(stall_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM reviews WHERE stall_id=? AND user_id=?", (stall_id, user_id))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def is_favourited(stall_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM favourites WHERE stall_id=? AND user_id=?",
        (stall_id, user_id)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def toggle_favourite_db(stall_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM favourites WHERE stall_id=? AND user_id=?",
        (stall_id, user_id)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "DELETE FROM favourites WHERE stall_id=? AND user_id=?",
            (stall_id, user_id)
        )
    else:
        cursor.execute(
            "INSERT INTO favourites (stall_id, user_id) VALUES (?, ?)",
            (stall_id, user_id)
        )

    conn.commit()
    conn.close()

def get_all_stalls():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stalls")
    stalls = cursor.fetchall()
    conn.close()
    return stalls

def get_stall(stall_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stalls WHERE id=?", (stall_id,))
    stall = cursor.fetchone()
    conn.close()
    return stall

def get_reviews(stall_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT reviews.*, users.username
    FROM reviews
    JOIN users ON reviews.user_id = users.id
    WHERE reviews.stall_id = ?
    ORDER BY reviews.created_at DESC
    """, (stall_id,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews


@ratings_bp.route("/rating")
def stall_list():
    stalls = get_all_stalls()
    stall_ratings = {}
    user_id = get_current_user_id()

    favourites = {}

    for stall in stalls:
        stall_ratings[stall["id"]] = get_average_rating(stall["id"])
        favourites[stall["id"]] = is_favourited(stall["id"], user_id)

    return render_template_string(
        STALL_LIST_PAGE,
        stalls=stalls,
        stall_ratings=stall_ratings,
        favourites=favourites
        )


@ratings_bp.route("/rating/<int:stall_id>")
def stall_detail(stall_id):
    stall = get_stall(stall_id)
    if not stall:
        return "Stall not found.", 404

    avg_rating = get_average_rating(stall_id)
    user_id = get_current_user_id()
    logged_in = is_logged_in()
    already_rated = user_already_rated(stall_id, user_id) if logged_in else False
    already_reviewed = user_already_reviewed(stall_id, user_id) if logged_in else False
    reviews = get_reviews(stall_id)
    admin = is_admin()


    user_rating = None
    if already_rated:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ratings WHERE stall_id=? AND user_id=?", (stall_id, user_id))
        user_rating = cursor.fetchone()
        conn.close()

    return render_template_string(STALL_DETAIL_PAGE,
        stall=stall,
        avg_rating=avg_rating,
        already_rated=already_rated,
        already_reviewed=already_reviewed,
        user_rating=user_rating,
        user_id=user_id,
        logged_in=logged_in,
        reviews=reviews,
        is_admin=admin
    )


@ratings_bp.route("/rating/<int:stall_id>/rate", methods=["POST"])
def add_rating(stall_id):
    if not is_logged_in():
        return redirect(url_for("ratings.stall_detail", stall_id=stall_id))

    user_id = get_current_user_id()

    if user_already_rated(stall_id, user_id):
        return "You already rated this stall.", 400

    rating = request.form.get("rating", "").strip()
    if not rating:
        return "Rating is required.", 400

    rating = int(rating)
    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5.", 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (stall_id, user_id, rating) VALUES (?, ?, ?)", (stall_id, user_id, rating))
    conn.commit()
    conn.close()

    return redirect(url_for("ratings.stall_detail", stall_id=stall_id))


@ratings_bp.route("/rating/<int:stall_id>/rate/edit", methods=["POST"])
def edit_rating(stall_id):
    user_id = get_current_user_id()

    rating = request.form.get("rating", "").strip()
    if not rating:
        return "Rating is required.", 400

    rating = int(rating)
    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5.", 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE ratings SET rating=? WHERE stall_id=? AND user_id=?", (rating, stall_id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for("ratings.stall_detail", stall_id=stall_id))


@ratings_bp.route("/rating/<int:stall_id>/rate/delete", methods=["POST"])
def delete_rating(stall_id):
    user_id = get_current_user_id()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ratings WHERE stall_id=? AND user_id=?", (stall_id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for("ratings.stall_detail", stall_id=stall_id))

# review
@ratings_bp.route("/rating/<int:stall_id>/review/add", methods=["POST"])
def add_review(stall_id):
    if not is_logged_in():
        return redirect(url_for("ratings.stall_detail", stall_id=stall_id))
    user_id = get_current_user_id()
    if user_already_reviewed(stall_id, user_id):
        return "You already reviewed this stall.", 400
    comment = request.form.get("comment", "").strip()
    if not comment:
        return "Comment is required.", 400
    if len(comment) < 20:
        return "Review must be at least 20 characters.", 400
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (stall_id, user_id, comment) VALUES (?, ?, ?)", (stall_id, user_id, comment))
    conn.commit()
    conn.close()
    return redirect(url_for("ratings.stall_detail", stall_id=stall_id))

@ratings_bp.route("/favourite/<int:stall_id>", methods=["POST"])
def toggle_favourite(stall_id):
    if not is_logged_in():
        return redirect(url_for("ratings.stall_list"))

    user_id = get_current_user_id()
    toggle_favourite_db(stall_id, user_id)

    return redirect(request.referrer or url_for("ratings.stall_list"))

@ratings_bp.route("/rating/<int:stall_id>/review/edit/<int:review_id>", methods=["POST"])
def edit_review(stall_id, review_id):
    user_id = get_current_user_id()
    comment = request.form.get("comment", "").strip()
    if not comment:
        return "Comment is required.", 400
    if len(comment) < 20:
        return "Review must be at least 20 characters.", 400
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE reviews SET comment=? WHERE id=? AND user_id=?", (comment, review_id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("ratings.stall_detail", stall_id=stall_id))


@ratings_bp.route("/rating/<int:stall_id>/review/delete/<int:review_id>", methods=["POST"])
def delete_review(stall_id, review_id):
    user_id = get_current_user_id()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if is_admin():
        cursor.execute("DELETE FROM reviews WHERE id=?", (review_id,))
    else:
        cursor.execute("DELETE FROM reviews WHERE id=? AND user_id=?", (review_id, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for("ratings.stall_detail", stall_id=stall_id))


STALL_LIST_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Food Stalls</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'DM Sans', sans-serif; background: #0f0f0f; color: #f0ede6; min-height: 100vh; padding: 40px 20px; }
h2 { font-family: 'Syne', sans-serif; font-size: 2.5rem; font-weight: 800; margin-bottom: 8px; }
.subtitle { color: #888; font-size: 0.95rem; margin-bottom: 40px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }
.card { background: #1a1a1a; border-radius: 16px; overflow: hidden; transition: transform 0.2s ease, box-shadow 0.2s ease; border: 1px solid #2a2a2a; }
.card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
.card-img { width: 100%; height: 160px; background: linear-gradient(135deg, #2a2a2a, #1f1f1f, #2e2a1f); display: flex; align-items: center; justify-content: center; font-size: 3rem; }
.card-body { padding: 16px; }
.card-name { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; }
.card-meta { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.tag { font-size: 0.72rem; padding: 3px 8px; border-radius: 20px; background: #2a2a2a; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; }
.tag.price { background: #1f2a1f; color: #7ecb7e; }
.card-rating { font-size: 0.9rem; color: #f5c842; margin-bottom: 14px; font-weight: 500; }
.btn { display: block; width: 100%; padding: 10px; background: #f5c842; color: #0f0f0f; text-align: center; border-radius: 10px; font-weight: 700; font-size: 0.85rem; text-decoration: none; font-family: 'Syne', sans-serif; transition: background 0.15s ease; }
.btn:hover { background: #f0b800; }
.back-link { display: inline-block; margin-top: 40px; color: #888; text-decoration: none; font-size: 0.9rem; }
.back-link:hover { color: #f0ede6; }
</style>
</head>
<body>
<div style="max-width:1100px; margin:0 auto;">
<h2>🍴 Food Stalls</h2>
<p class="subtitle">Find your next meal — rate and review what you've tried</p>
<div class="grid">
{% for stall in stalls %}
<div class="card">
<div class="card-img">🍽️</div>
<div class="card-body">
<form method="POST" action="/favourite/{{ stall.id }}" style="text-align:right;">
<button type="submit" style="background:none;border:none;font-size:1.4rem;cursor:pointer;">
{% if favourites[stall.id] %}
❤️
{% else %}
🤍
{% endif %}
</button>
</form>
<div class="card-name">{{ stall.name }}</div>
<div class="card-meta">
<span class="tag">{{ stall.category }}</span>
<span class="tag price">{{ stall.price_range }}</span>
</div>
<div class="card-rating">
{% if stall_ratings[stall.id] %}⭐ {{ stall_ratings[stall.id] }} / 5{% else %}No ratings yet{% endif %}
</div>
<a class="btn" href="/rating/{{ stall.id }}">View & Rate</a>
</div>
</div>
{% endfor %}
</div>
<a class="back-link" href="/quiz">← Back to Quiz</a>
</div>
</body>
</html>
"""

STALL_DETAIL_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{{ stall.name }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'DM Sans', sans-serif; background: #0f0f0f; color: #f0ede6; min-height: 100vh; padding: 40px 20px; }
.container { max-width: 680px; margin: 0 auto; }
.hero { width: 100%; height: 220px; background: linear-gradient(135deg, #2a2a2a, #1f1f1f, #2e2a1f); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 5rem; margin-bottom: 24px; }
h2 { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
h3 { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; }
.meta { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.tag { font-size: 0.72rem; padding: 3px 10px; border-radius: 20px; background: #2a2a2a; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; }
.tag.price { background: #1f2a1f; color: #7ecb7e; }
.desc { color: #999; font-size: 0.95rem; margin-bottom: 20px; }
.avg-rating { font-size: 1.5rem; font-family: 'Syne', sans-serif; font-weight: 700; color: #f5c842; margin-bottom: 32px; }
hr { border: none; border-top: 1px solid #2a2a2a; margin: 28px 0; }
.box { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
select { background: #2a2a2a; color: #f0ede6; border: 1px solid #3a3a3a; border-radius: 8px; padding: 8px 12px; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; cursor: pointer; margin-right: 8px; }
textarea { width: 100%; background: #2a2a2a; color: #f0ede6; border: 1px solid #3a3a3a; border-radius: 8px; padding: 10px 12px; font-family: 'DM Sans', sans-serif; font-size: 0.9rem; resize: vertical; margin-top: 8px; }
label { display: block; margin-bottom: 6px; color: #aaa; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }
.btn { padding: 10px 20px; background: #f5c842; color: #0f0f0f; border: none; border-radius: 10px; font-weight: 700; font-size: 0.85rem; cursor: pointer; font-family: 'Syne', sans-serif; transition: background 0.15s; }
.btn:hover { background: #f0b800; }
.btn-ghost { padding: 8px 16px; background: transparent; color: #aaa; border: 1px solid #3a3a3a; border-radius: 8px; font-size: 0.8rem; cursor: pointer; font-family: 'DM Sans', sans-serif; transition: all 0.15s; margin-left: 8px; }
.btn-ghost:hover { border-color: #f0ede6; color: #f0ede6; }
.btn-danger { padding: 8px 16px; background: transparent; color: #e05555; border: 1px solid #e05555; border-radius: 8px; font-size: 0.8rem; cursor: pointer; font-family: 'DM Sans', sans-serif; transition: all 0.15s; margin-left: 8px; }
.btn-danger:hover { background: #e05555; color: white; }
color: #f5c842; text-decoration: none; }
/* review cards */
.review-card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 16px; margin-bottom: 12px; position: relative; }
.review-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.review-username { font-weight: 700; font-size: 0.95rem; color: #f0ede6; }
.review-date { font-size: 0.75rem; color: #666; margin-top: 2px; }
.review-comment { color: #ccc; font-size: 0.9rem; line-height: 1.6; }
/* 3-dot menu */
.menu-wrap { position: relative; }
.menu-btn { background: none; border: none; color: #666; font-size: 1.2rem; cursor: pointer; padding: 4px 8px; border-radius: 6px; transition: background 0.15s; }
.menu-btn:hover { background: #2a2a2a; color: #f0ede6; }
.dropdown { display: none; position: absolute; right: 0; top: 100%; background: #222; border: 1px solid #333; border-radius: 10px; min-width: 130px; z-index: 10; overflow: hidden; }
.menu-wrap:hover .dropdown { display: block; }
.dropdown form { margin: 0; }
.dropdown button { width: 100%; padding: 10px 14px; background: none; border: none; color: #f0ede6; font-size: 0.85rem; text-align: left; cursor: pointer; font-family: 'DM Sans', sans-serif; transition: background 0.1s; display: flex; align-items: center; gap: 8px; }
.dropdown button:hover { background: #2a2a2a; }
.dropdown button.danger { color: #e05555; }
.dropdown button.danger:hover { background: #2a1a1a; }
/* inline edit form */
.edit-form { display: none; margin-top: 10px; }
                                                                                                                .edit-form.active { display: block; }

                                                                                                                .back-link { display: inline-block; margin-top: 32px; color: #888; text-decoration: none; font-size: 0.9rem; }
                                                                                                                    .back-link:hover { color: #f0ede6; }
                                                                                                                        .char-count { font-size: 0.75rem; color: #666; margin-top: 4px; }
                                                                                                                            </style>
                                                                                                                            </head>
                                                                                                                            <body>
                                                                                                                            <div class="container">
                                                                                                                            <div class="hero">🍽️</div>
                                                                                                                            <h2>{{ stall.name }}</h2>
                                                                                                                            <div class="meta">
                                                                                                                            <span class="tag">{{ stall.category }}</span>
                                                                                                                            <span class="tag price">{{ stall.price_range }}</span>
                                                                                                                            </div>
                                                                                                                            <p class="desc">{{ stall.description }}</p>
                                                                                                                            <div class="avg-rating">
                                                                                                                            {% if avg_rating %}⭐ {{ avg_rating }} / 5{% else %}No ratings yet{% endif %}
                                                                                                                            </div>

                                                                                                                            <hr>

                                                                                                                            <!-- RATING SECTION -->
                                                                                                                            <h3>Rate This Stall</h3>
                                                                                                                            {% if logged_in %}
                                                                                                                            {% if already_rated %}
                                                                                                                            <div class="box">
                                                                                                                            <p style="color:#f5c842; margin-bottom:12px;">Your rating: {{ user_rating.rating }}/5 ⭐</p>
                                                                                                                                <form method="POST" action="/rating/{{ stall.id }}/rate/edit" style="display:inline">
                                                                                                                                <select name="rating" required>
                                                                                                                                <option value="5" {{ 'selected' if user_rating.rating == 5 }}>⭐⭐⭐⭐⭐ (5)</option>
                                                                                                                                <option value="4" {{ 'selected' if user_rating.rating == 4 }}>⭐⭐⭐⭐ (4)</option>
                                                                                                                                <option value="3" {{ 'selected' if user_rating.rating == 3 }}>⭐⭐⭐ (3)</option>
                                                                                                                                <option value="2" {{ 'selected' if user_rating.rating == 2 }}>⭐⭐ (2)</option>
                                                                                                                                <option value="1" {{ 'selected' if user_rating.rating == 1 }}>⭐ (1)</option>
                                                                                                                                </select>
                                                                                                                                <button class="btn" type="submit">Update</button>
                                                                                                                                </form>
                                                                                                                                <form method="POST" action="/rating/{{ stall.id }}/rate/delete" style="display:inline">
                                                                                                                                <button class="btn-danger" type="submit" onclick="return confirm('Remove your rating?')">Remove</button>
                                                                                                                                </form>
                                                                                                                                </div>
                                                                                                                                {% else %}
                                                                                                                                <div class="box">
                                                                                                                                <form method="POST" action="/rating/{{ stall.id }}/rate">
                                                                                                                                <label>Pick your rating</label>
                                                                                                                                <select name="rating" required>
                                                                                                                                <option value="">-- Pick --</option>
                                                                                                                                <option value="5">⭐⭐⭐⭐⭐ (5)</option>
                                                                                                                                <option value="4">⭐⭐⭐⭐ (4)</option>
                                                                                                                                <option value="3">⭐⭐⭐ (3)</option>
                                                                                                                                <option value="2">⭐⭐ (2)</option>
                                                                                                                                <option value="1">⭐ (1)</option>
                                                                                                                                </select>
                                                                                                                                <button class="btn" type="submit">Submit</button>
                                                                                                                                </form>
                                                                                                                                </div>
                                                                                                                                {% endif %}
                                                                                                                                {% else %}
                                                                                                                                <div class="login-prompt">Please <a href="/login">log in</a> to rate this stall.</div>
                                                                                                                                {% endif %}

                                                                                                                                <hr>

                                                                                                                                <!-- REVIEWS SECTION -->
                                                                                                                                <h3>Reviews ({{ reviews|length }})</h3>

                                                                                                                                {% if reviews %}
                                                                                                                                {% for r in reviews %}
                                                                                                                                <div class="review-card">
                                                                                                                                <div class="review-header">
                                                                                                                                <div>
                                                                                                                                <div class="review-username">{{ r.username }}</div>
                                                                                                                                <div class="review-date">{{ r.created_at }}</div>
                                                                                                                                </div>
                                                                                                                                {% if logged_in and (r.user_id == user_id or is_admin) %}
                                                                                                                                <div class="menu-wrap">
                                                                                                                                <button class="menu-btn">⋯</button>
                                                                                                                                <div class="dropdown">
                                                                                                                                {% if r.user_id == user_id %}
                                                                                                                                <button type="button" onclick="toggleEdit('edit-{{ r.id }}')">✏️ Edit</button>
                                                                                                                                {% endif %}
                                                                                                                                <form method="POST" action="/rating/{{ stall.id }}/review/delete/{{ r.id }}">
                                                                                                                                <button class="danger" type="submit" onclick="return confirm('Delete this review?')">🗑️ Delete</button>
                                                                                                                                </form>
                                                                                                                                </div>
                                                                                                                                </div>
                                                                                                                                {% endif %}
                                                                                                                                </div>
                                                                                                                                <p class="review-comment">{{ r.comment }}</p>

                                                                                                                                <!-- inline edit form -->
                                                                                                                                {% if logged_in and r.user_id == user_id %}
                                                                                                                                <div class="edit-form" id="edit-{{ r.id }}">
                                                                                                                                <form method="POST" action="/rating/{{ stall.id }}/review/edit/{{ r.id }}">
                                                                                                                                <textarea name="comment" rows="3" minlength="20" required>{{ r.comment }}</textarea>
                                                                                                                                <p class="char-count">Minimum 20 characters</p>
                                                                                                                                <button class="btn" type="submit" style="margin-top:8px;">Save</button>
                                                                                                                                <button class="btn-ghost" type="button" onclick="toggleEdit('edit-{{ r.id }}')">Cancel</button>
                                                                                                                                </form>
                                                                                                                                </div>
                                                                                                                                {% endif %}
                                                                                                                                </div>
                                                                                                                                {% endfor %}
                                                                                                                                {% else %}
                                                                                                                                <p style="color:#666; font-size:0.9rem;">No reviews yet. Be the first!</p>
                                                                                                                                    {% endif %}

                                                                                                                                    <hr>

                                                                                                                                    <!-- WRITE REVIEW -->
                                                                                                                                    <h3>Write a Review</h3>
                                                                                                                                    {% if logged_in %}
                                                                                                                                    {% if already_reviewed %}
                                                                                                                                    <p style="color:#888; font-size:0.9rem;">You already reviewed this stall. Edit it above.</p>
                                                                                                                                        {% else %}
                                                                                                                                        <div class="box">
                                                                                                                                        <form method="POST" action="/rating/{{ stall.id }}/review/add">
                                                                                                                                        <label>Your Review (min. 20 characters)</label>
                                                                                                                                        <textarea name="comment" rows="4" minlength="20" required placeholder="What did you think of this place?"></textarea>
                                                                                                                                        <p class="char-count" id="charCount">0 / 20 minimum</p>
                                                                                                                                        <button class="btn" type="submit" style="margin-top:12px; display:block; width:100%;">Post Review</button>
                                                                                                                                        </form>
                                                                                                                                        </div>
                                                                                                                                        {% endif %}
                                                                                                                                        {% else %}
                                                                                                                                        <div class="login-prompt">Please <a href="/login">log in</a> to write a review.</div>
                                                                                                                                        {% endif %}

                                                                                                                                        <a class="back-link" href="/rating">← Back to Stalls</a>
                                                                                                                                        </div>

                                                                                                                                        <script>
                                                                                                                                        function toggleEdit(id) {
                                                                                                                                            const el = document.getElementById(id);
                                                                                                                                            el.classList.toggle('active');
                                                                                                                                        }

                                                                                                                                        // character counter for review textarea
                                                                                                                                        const ta = document.querySelector('textarea[name="comment"]');
                                                                                                                                        const cc = document.getElementById('charCount');
                                                                                                                                        if (ta && cc) {
                                                                                                                                            ta.addEventListener('input', () => {
                                                                                                                                                const len = ta.value.length;
                                                                                                                                                cc.textContent = len + ' / 20 minimum';
                                                                                                                                                cc.style.color = len >= 20 ? '#7ecb7e' : '#666';
                                                                                                                                            });
                                                                                                                                        }
                                                                                                                                        </script>
                                                                                                                                        </body>
                                                                                                                                        </html>
                                                                                                                                        """