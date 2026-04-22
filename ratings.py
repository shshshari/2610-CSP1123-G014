import sqlite3
from flask import Blueprint, render_template_string, request, redirect, url_for, session

ratings_bp = Blueprint("ratings", __name__)
DB_PATH = "stalls.db"


def get_current_user_id():
    return session.get("user_id", 1) 

def is_logged_in():
    return True  

# def get_current_user_id():
#    return session.get("user_id")  

#def is_logged_in():
#    return "user_id" in session  

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




@ratings_bp.route("/rating")
def stall_list():
    stalls = get_all_stalls()
    stall_ratings = {}
    for stall in stalls:
        stall_ratings[stall["id"]] = get_average_rating(stall["id"])
    return render_template_string(STALL_LIST_PAGE, stalls=stalls, stall_ratings=stall_ratings)


@ratings_bp.route("/rating/<int:stall_id>")
def stall_detail(stall_id):
    stall = get_stall(stall_id)
    if not stall:
        return "Stall not found.", 404

    avg_rating = get_average_rating(stall_id)
    user_id = get_current_user_id()
    already_rated = user_already_rated(stall_id, user_id)

    # get user's existing rating if any
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
        user_rating=user_rating,
        user_id=user_id
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


# html replace with meera's later

STALL_LIST_PAGE = """
<h2>🍴 Food Stalls</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Name</th>
        <th>Category</th>
        <th>Price</th>
        <th>Avg Rating</th>
        <th></th>
    </tr>
    {% for stall in stalls %}
    <tr>
        <td>{{ stall.name }}</td>
        <td>{{ stall.category }}</td>
        <td>{{ stall.price_range }}</td>
        <td>{{ stall_ratings[stall.id] if stall_ratings[stall.id] else 'No ratings yet' }} ⭐</td>
        <td><a href="/rating/{{ stall.id }}">View & Rate</a></td>
    </tr>
    {% endfor %}
</table>
<br>
<a href="/quiz">← Back to Quiz</a>
"""

STALL_DETAIL_PAGE = """
<h2>{{ stall.name }}</h2>
<p>Category: {{ stall.category }} | Price: {{ stall.price_range }}</p>
<p>{{ stall.description }}</p>

<h3>⭐ Average Rating: {{ avg_rating if avg_rating else 'No ratings yet' }} / 5</h3>

<hr>
<h3>Your Rating</h3>

{% if already_rated %}
    <p>You rated this stall: {{ user_rating.rating }}/5 ⭐</p>

    <form method="POST" action="/rating/{{ stall.id }}/rate/edit" style="display:inline">
        Change rating:
        <select name="rating" required>
            <option value="5" {{ 'selected' if user_rating.rating == 5 }}>⭐⭐⭐⭐⭐ (5)</option>
            <option value="4" {{ 'selected' if user_rating.rating == 4 }}>⭐⭐⭐⭐ (4)</option>
            <option value="3" {{ 'selected' if user_rating.rating == 3 }}>⭐⭐⭐ (3)</option>
            <option value="2" {{ 'selected' if user_rating.rating == 2 }}>⭐⭐ (2)</option>
            <option value="1" {{ 'selected' if user_rating.rating == 1 }}>⭐ (1)</option>
        </select>
        <button type="submit">Update</button>
    </form>

    <form method="POST" action="/rating/{{ stall.id }}/rate/delete" style="display:inline">
        <button type="submit" onclick="return confirm('Remove your rating?')">Remove Rating</button>
    </form>

{% else %}
    <form method="POST" action="/rating/{{ stall.id }}/rate">
        Rate this stall:
        <select name="rating" required>
            <option value="">-- Pick --</option>
            <option value="5">⭐⭐⭐⭐⭐ (5)</option>
            <option value="4">⭐⭐⭐⭐ (4)</option>
            <option value="3">⭐⭐⭐ (3)</option>
            <option value="2">⭐⭐ (2)</option>
            <option value="1">⭐ (1)</option>
        </select>
        <button type="submit">Submit Rating</button>
    </form>
{% endif %}

<br><a href="/rating">← Back to Stalls</a>
"""
