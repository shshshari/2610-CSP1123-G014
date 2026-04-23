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


STALL_LIST_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Food Stalls</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'DM Sans', sans-serif;
    background: #0f0f0f;
        color: #f0ede6;
            min-height: 100vh;
            padding: 40px 20px;
        }

        h2 {
            font-family: 'Syne', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 8px;
            color: #f0ede6;
            }

            .subtitle {
                color: #888;
                    font-size: 0.95rem;
                    margin-bottom: 40px;
                }

                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
                    gap: 20px;
                    max-width: 1100px;
                    margin: 0 auto;
                }

                .card {
                    background: #1a1a1a;
                        border-radius: 16px;
                        overflow: hidden;
                        transition: transform 0.2s ease, box-shadow 0.2s ease;
                        border: 1px solid #2a2a2a;
                    }

                    .card:hover {
                        transform: translateY(-4px);
                        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
                    }

                    .card-img {
                        width: 100%;
                        height: 160px;
                        object-fit: cover;
                        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 50%, #2e2a1f 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 3rem;
                    }

                    .card-body {
                        padding: 16px;
                    }

                    .card-name {
                        font-family: 'Syne', sans-serif;
                        font-size: 1.1rem;
                        font-weight: 700;
                        margin-bottom: 6px;
                        color: #f0ede6;
                        }

                        .card-meta {
                            display: flex;
                            gap: 8px;
                            margin-bottom: 12px;
                            flex-wrap: wrap;
                        }

                        .tag {
                            font-size: 0.72rem;
                            padding: 3px 8px;
                            border-radius: 20px;
                            background: #2a2a2a;
                                color: #aaa;
                                    text-transform: uppercase;
                                    letter-spacing: 0.5px;
                                }

                                .tag.price { background: #1f2a1f; color: #7ecb7e; }

                                    .card-rating {
                                        font-size: 0.9rem;
                                        color: #f5c842;
                                            margin-bottom: 14px;
                                            font-weight: 500;
                                        }

                                        .btn {
                                            display: block;
                                            width: 100%;
                                            padding: 10px;
                                            background: #f5c842;
                                                color: #0f0f0f;
                                                    text-align: center;
                                                    border-radius: 10px;
                                                    font-weight: 700;
                                                    font-size: 0.85rem;
                                                    text-decoration: none;
                                                    font-family: 'Syne', sans-serif;
                                                    letter-spacing: 0.3px;
                                                    transition: background 0.15s ease;
                                                }

                                                .btn:hover { background: #f0b800; }

                                                    .back-link {
                                                        display: inline-block;
                                                        margin-top: 40px;
                                                        color: #888;
                                                            text-decoration: none;
                                                            font-size: 0.9rem;
                                                            transition: color 0.15s;
                                                        }

                                                        .back-link:hover { color: #f0ede6; }
                                                            </style>
                                                            </head>
                                                            <body>
                                                            <div style="max-width:1100px; margin:0 auto;">
                                                            <h2>🍴 Food Stalls</h2>
<p class="subtitle">Hi I dont know what to write here</p>

                                                            <div class="grid">
                                                            {% for stall in stalls %}
                                                            <div class="card">
                                                            <div class="card-img">🍽️</div>
                                                            <div class="card-body">
                                                            <div class="card-name">{{ stall.name }}</div>
                                                            <div class="card-meta">
                                                            <span class="tag">{{ stall.category }}</span>
                                                            <span class="tag price">{{ stall.price_range }}</span>
                                                            </div>
                                                            <div class="card-rating">
                                                            {% if stall_ratings[stall.id] %}
                                                            ⭐ {{ stall_ratings[stall.id] }} / 5
                                                            {% else %}
                                                            No ratings yet
                                                            {% endif %}
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

body {
    font-family: 'DM Sans', sans-serif;
    background: #0f0f0f;
        color: #f0ede6;
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container { max-width: 640px; margin: 0 auto; }

        .hero {
            width: 100%;
            height: 220px;
            background: linear-gradient(135deg, #2a2a2a, #1f1f1f, #2e2a1f);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 5rem;
            margin-bottom: 24px;
        }

        h2 {
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .meta {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .tag {
            font-size: 0.72rem;
            padding: 3px 10px;
            border-radius: 20px;
            background: #2a2a2a;
                color: #aaa;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

        .tag.price { background: #1f2a1f; color: #7ecb7e; }

        .desc { color: #999; font-size: 0.95rem; margin-bottom: 20px; }

        .avg-rating {
                            font-size: 1.5rem;
                            font-family: 'Syne', sans-serif;
                            font-weight: 700;
                            color: #f5c842;
                                margin-bottom: 32px;
                            }

        hr { border: none; border-top: 1px solid #2a2a2a; margin: 24px 0; }

        h3 {
                                font-family: 'Syne', sans-serif;
                                font-size: 1.1rem;
                                font-weight: 700;
                                margin-bottom: 16px;
                                color: #f0ede6;
                                }

        .your-rating {
                                    background: #1a1a1a;
                                        border: 1px solid #2a2a2a;
                                        border-radius: 12px;
                                        padding: 16px;
                                        margin-bottom: 16px;
                                    }

        .your-rating p { margin-bottom: 12px; color: #f5c842; font-weight: 500; }

        select {
background: #2a2a2a;
color: #f0ede6;
border: 1px solid #3a3a3a;
border-radius: 8px;
padding: 8px 12px;
font-family: 'DM Sans', sans-serif;
font-size: 0.9rem;
cursor: pointer;
margin-right: 8px;
                   }

    .btn {
padding: 10px 20px;
background: #f5c842;
color: #0f0f0f;
border: none;
border-radius: 10px;
font-weight: 700;
font-size: 0.85rem;
cursor: pointer;
font-family: 'Syne', sans-serif;
transition: background 0.15s;
}

.btn:hover { background: #f0b800; }

.btn-danger {
padding: 10px 20px;
background: transparent;
color: #e05555;
border: 1px solid #e05555;
border-radius: 10px;
font-weight: 600;
font-size: 0.85rem;
cursor: pointer;
font-family: 'DM Sans', sans-serif;
transition: all 0.15s;
margin-left: 8px;
}

.btn-danger:hover { background: #e05555; color: white; }
.rate-form {
                                                                        background: #1a1a1a;
                                                                            border: 1px solid #2a2a2a;
                                                                            border-radius: 12px;
                                                                            padding: 20px;
                                                                        }

                                                                        .rate-form label {
display: block;
margin-bottom: 8px;
color: #aaa;
font-size: 0.85rem;
                                                                                text-transform: uppercase;
                                                                                letter-spacing: 0.5px;
                                                                            }

                                                                            .back-link {
                                                                                display: inline-block;
                                                                                margin-top: 32px;
                                                                                color: #888;
                                                                                    text-decoration: none;
                                                                                    font-size: 0.9rem;
                                                                                    transition: color 0.15s;
                                                                                }

                                                                                .back-link:hover { color: #f0ede6; }
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
                                                                                    <h3>Your Rating</h3>

                                                                                    {% if already_rated %}
                                                                                    <div class="your-rating">
                                                                                    <p>You rated this: {{ user_rating.rating }}/5 ⭐</p>
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
                                                                                    <div class="rate-form">
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
                                                                                    <button class="btn" type="submit" style="margin-top:12px; display:block; width:100%;">Submit Rating</button>
                                                                                    </form>
                                                                                    </div>
                                                                                    {% endif %}

                                                                                    <a class="back-link" href="/rating">← Back to Stalls</a>
                                                                                    </div>
                                                                                    </body>
                                                                                    </html>
                                                                                    """