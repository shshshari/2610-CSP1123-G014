from flask import Flask, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "replace_with_a_random_secret_key"

HTML_HOMEPAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MMU Food Recommender</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style2.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
            <h1 class="logo">
                <img src="{{ url_for('static', filename='foodstall.png') }}" alt=""> MMU Food Recommender
            </h1>
    <header>
        <div class="container">


            <nav>
                <ul class="nav-list">
                    <li><a href="{{ url_for('index') }}">Home</a></li>
                    <li><a href="#search">Search</a></li>
                </ul>
            </nav>

            <div class="hamburger" id="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="dropdown-menu" id="dropdownMenu">
                <a href="#">Favourite</a>
                <a href="#">Review</a>
                <a href="#">Profile</a>
                {% if logged_in %}
                    <a href="#">Sign Out</a>
                {% else %}
                    <a href="#">Sign In</a>
                {% endif %}
            </div>
        </div>
    </header>

    <section class="hero" id="search">
        <div class="hero-section">
            <h1>Welcome to our Food Recommender System</h1>
            <form action="#search" class="search-box">
                <input type="text" placeholder="Search 🔍">
                <button type="submit">Search</button>
            </form>
            <div class="filter-button">
                <button class="filter-btn">Range</button>
                <button class="filter-btn">Category</button>
                <button class="filter-btn">Ratings</button>
            </div>
        </div>
    </section>

    <section class="stalls">
        <h1>Featured Stalls</h1>
        <div class="stall-section">

            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall1.jpeg') }}" alt="">
                <h2>JINJJA SHYOK</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="1">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('1', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall2.jpeg') }}" alt="">
                <h2>CITA RASA</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="2">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('2', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall3.jpg') }}" alt="">
                <h2>STALL 3</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="3">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('3', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 4</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="4">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('4', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

        </div>
    </section>

    <script>
    const hamburger = document.getElementById('hamburger');
    const menu = document.getElementById('dropdownMenu');

    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        menu.classList.toggle('open');
    });

    document.addEventListener('click', function(e) {
        if (!menu.contains(e.target) && !hamburger.contains(e.target)) {
            menu.classList.remove('open');
        }
    });
    </script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if "colors" not in session:
        session["colors"] = {}

    if request.method == "POST":
        stall_id = request.form.get("stall")
        if stall_id:
            colors = session["colors"]
            colors[stall_id] = "#e74c3c" if colors.get(stall_id) != "#e74c3c" else "#ccc"
            session["colors"] = colors

    logged_in = session.get("logged_in", False)

    return render_template_string(HTML_HOMEPAGE, colors=session.get("colors", {}), logged_in=logged_in)

if __name__ == "__main__":
    app.run(debug=True)