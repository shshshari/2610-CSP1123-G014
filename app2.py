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

            <label class="hamburger" for="menu-toggle">
                <span></span>
                <span></span>
                <span></span>
            </label>
            <input type="checkbox" id="menu-toggle">
            <div class="dropdown-menu">
                <a href="#">Favourite</a>
                <a href="#">Review</a>
                <a href="{{ url_for('profile') }}">Profile</a>
            {% if logged_in %}
                <a href="{{ url_for('logout') }}">Sign Out</a>
            {% else %}
                <a href="{{ url_for('login') }}">Sign In</a>
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

             <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 5</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="4">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('4', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

             <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 6</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="4">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('4', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

             <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 7</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="4">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('4', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

             <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 8</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="4">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('4', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

        </div>
    </section>

</body>
</html>
"""

HTML_PROFILE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Profile - MMU Food Recommender</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='profile.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
 
    <header>
        <div class="container">
            <nav>
                <ul class="nav-list">
                    <li><a href="{{ url_for('index') }}">Home</a></li>
                    <li><a href="#search">Search</a></li>
                </ul>
            </nav>
    <header>
        
            <div class="nav-right">
                <span class="profile-label">Profile</span>
                <label class="hamburger" for="menu-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </label>
                <input type="checkbox" id="menu-toggle">
                <div class="dropdown-menu">
                    <a href="{{ url_for('index') }}">Home</a>
                    <a href="#">Favourite</a>
                    <a href="#">Review</a>
                    <a href="{{ url_for('profile') }}">Profile</a>
                    {% if logged_in %}
                        <a href="#">Sign Out</a>
                    {% else %}
                        <a href="#">Sign In</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </header>

    <section class="profile-section">
        <div class="profile-card">
            <div class="avatar">
                <i class="fa fa-user"></i>
            </div>
            <div class="profile-info">
                <h2 class="profile-name">Name</h2>
                <p class="profile-bio">Bio</p>
                <button class="btn-edit">Edit Profile</button>
                <button class="btn-logout">Logout</button>
            </div>
        </div>
    </section>

    <div class="wavy-divider">
        <svg viewBox="0 0 1200 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0,30 C50,0 100,60 150,30 C200,0 250,60 300,30 C350,0 400,60 450,30 C500,0 550,60 600,30 C650,0 700,60 750,30 C800,0 850,60 900,30 C950,0 1000,60 1050,30 C1100,0 1150,60 1200,30"
                  stroke="#1c4273" stroke-width="2.5" fill="none"/>
        </svg>
    </div>

    <section class="bottom-section">
        <div class="column">
            <h3 class="column-title">- Fav Stalls -</h3>
            <div class="card-placeholder"></div>
            <div class="card-placeholder"></div>
        </div>
        <div class="column">
            <h3 class="column-title">- My Reviews -</h3>
            <div class="card-placeholder"></div>
            <div class="card-placeholder"></div>
        </div>
    </section>

</body>
</html>
"""

HTML_LOGIN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login Form</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style3.css') }}">
</head>
<body>
    <div class="container" id="container">

        <!-- SIGN UP FORM -->
        <div class="form-container sign-up">
            <form>
                <h1>Create Account</h1>
                <div class="social-icons">
                    <a href="#"></a>
                </div>
                <span>or use email</span>
                <input type="text" placeholder="Name">
                <input type="email" placeholder="Email">
                <input type="password" placeholder="Password">
                <button>Sign Up</button>
            </form>
        </div>

        <!-- SIGN IN FORM -->
        <div class="form-container sign-in">
            <form>
                <h1>Sign In</h1>
                <div class="social-icons">
                    <a href="#"></a>
                </div>
                <span>or use email and password</span>
                <input type="email" placeholder="Email">
                <input type="password" placeholder="Password">
                <a href="#">Forgot your password?</a>
                <button>Sign In</button>
            </form>
        </div>

        <!-- TOGGLE PANEL -->
        <div class="toggle-container">
            <div class="toggle">

                <div class="toggle-panel toggle-left">
                    <h1>Welcome Back!</h1>
                    <p>Enter your personal details</p>
                    <button class="hidden" id="login">Sign In</button>
                </div>

                <div class="toggle-panel toggle-right">
                    <h1>Hello!</h1>
                    <p>Register your personal details</p>
                    <button class="hidden" id="register">Sign Up</button>
                </div>

            </div>
        </div>

    </div>
    <a href="{{ url_for('index') }}" class="back-home">← Back to Home</a>
</body>
</html>
"""

HTML_REGISTER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Register - MMU Food Recommender</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style3.css') }}">
</head>
<body>

    <div class="container">
        <div class="form-container sign-up" style="width:100%; position:relative; opacity:1;">
            <form method="POST" action="{{ url_for('register') }}">
                <h1>Create Account</h1>
                <span>or use your email</span>
                <input type="text" name="name" placeholder="Name">
                <input type="email" name="email" placeholder="Email">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Sign Up</button>
                <p>Already have an account? <a href="{{ url_for('login') }}">Sign In</a></p>
            </form>
        </div>
    </div>

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


@app.route("/profile")
def profile():
    logged_in = session.get("logged_in", False)
    return render_template_string(HTML_PROFILE, logged_in=logged_in)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = True
        return render_template_string(HTML_HOMEPAGE, colors=session.get("colors", {}), logged_in=True)
    return render_template_string(HTML_LOGIN)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return render_template_string(HTML_LOGIN)
    return render_template_string(HTML_REGISTER)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return render_template_string(HTML_HOMEPAGE, colors=session.get("colors", {}), logged_in=False)


if __name__ == "__main__":
    app.run(debug=True)