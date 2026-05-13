from flask import Flask, render_template_string, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = "replace_with_a_random_secret_key"

# ─────────────────────────────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────────────────────────────
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
                {% if session.get('role') == 'manager' %}
                    <a href="#">Manager Dashboard</a>
                {% endif %}
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
            <div style="margin-top: 16px;">
                <a href="{{ url_for('suggest') }}" class="filter-btn" style="text-decoration:none;">
                    ❓ What Should I Eat?
                </a>
            </div>
        </div>
    </section>

    <section class="stalls">
        <h1>Featured Stalls</h1>
        <div class="stall-section">

            <!-- STALL 1: JINJJA SHYOK -->
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

            <!-- STALL 2: CITA RASA -->
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

            <!-- STALL 3: Rasa Shiokk — clicking goes to stall detail page -->
            <div class="stall-card">
                <a href="{{ url_for('rasa_stall') }}" style="text-decoration:none; color:inherit;">
                    <img src="{{ url_for('static', filename='stall3.jpg') }}" alt="">
                    <h2>Rasa Shiokk</h2>
                </a>
                <form method="POST">
                    <input type="hidden" name="stall" value="3">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('3', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <!-- STALL 4 -->
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

            <!-- STALL 5 -->
            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 5</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="5">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('5', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <!-- STALL 6 -->
            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 6</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="6">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('6', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <!-- STALL 7 -->
            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 7</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="7">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('7', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

            <!-- STALL 8 -->
            <div class="stall-card">
                <img src="{{ url_for('static', filename='stall4.jpg') }}" alt="">
                <h2>STALL 8</h2>
                <form method="POST">
                    <input type="hidden" name="stall" value="8">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('8', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

        </div>
    </section>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# LOGIN PAGE
# Handles both Sign In and Sign Up in one page via toggle panel.
# /register redirects here with #signup hash to auto-open Sign Up.
# ─────────────────────────────────────────────────────────────────
HTML_LOGIN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login – MMU Food Recommender</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style3.css') }}">
</head>
<body>

    <div class="container" id="container">

        <!-- SIGN UP FORM -->
        <div class="form-container sign-up">
            <form method="POST" action="{{ url_for('register') }}">

                <h1>Create Account</h1>
                <span>or use your email</span>

                <input type="text" name="name" placeholder="Name" required/>
                <input type="email" name="email" placeholder="Email" required/>
                <input type="password" name="password" placeholder="Password" required/>

                <!-- ROLE SELECTION -->
                <div class="role-select">
                    <label>Select Role</label>
                    <select name="role" required>
                        <option value="">Choose Role</option>
                        <option value="student">Student</option>
                        <option value="manager">Manager</option>
                    </select>
                </div>

                <button type="submit">Sign Up</button>

            </form>
        </div>

        <!-- SIGN IN FORM -->
        <div class="form-container sign-in">
            <form method="POST" action="{{ url_for('login') }}">

                <h1>Sign In</h1>
                <span>or use your email and password</span>

                <input type="email" name="email" placeholder="Email" required/>
                <input type="password" name="password" placeholder="Password" required/>
        

                <a href="#">Forgot your password?</a>

                <button type="submit">Sign In</button>

            </form>
        </div>

        <!-- TOGGLE PANEL -->
        <div class="toggle-container">
            <div class="toggle">

                <div class="toggle-panel toggle-left">
                    <h1>Welcome Back!</h1>
                    <p>Enter your personal details to sign in</p>
                    <button type="button" id="loginToggle">Sign In</button>
                </div>

                <div class="toggle-panel toggle-right">
                    <h1>Hello!</h1>
                    <p>Register your personal details to get started</p>
                    <button type="button" id="registerToggle">Sign Up</button>
                </div>

            </div>
        </div>

    </div>

    <a href="{{ url_for('index') }}" class="back-home">← Back to Home</a>

    <script>
        const container = document.getElementById('container');
        const registerToggle = document.getElementById('registerToggle');
        const loginToggle = document.getElementById('loginToggle');

        registerToggle.addEventListener('click', () => {
            container.classList.add('active');
        });

        loginToggle.addEventListener('click', () => {
            container.classList.remove('active');
        });

        if (window.location.hash === '#signup') {
            container.classList.add('active');
        }
    </script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# WHAT SHOULD I EAT — SUGGEST PAGE
# ─────────────────────────────────────────────────────────────────
HTML_SUGGEST = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>What Should I Eat? – MMU Food Recommender</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="{{ url_for('static', filename='suggest.css') }}"/>
</head>
<body>

<nav>
  <div class="nav-logo">MMU Food Recommender System</div>
  <div class="nav-right">
    <a href="{{ url_for('profile') }}">Profile</a>
    <div class="hamburger"><span></span><span></span><span></span></div>
  </div>
</nav>

<main>

  <button class="back-btn" onclick="history.back()">← Back</button>

  <div class="trigger-wrapper">
    <button class="trigger-btn" id="triggerBtn" onclick="showQuiz()">
      <span class="trigger-icon">?</span>
      What Should I Eat?
    </button>
  </div>

  <div class="quiz-section" id="quizSection">

    <div class="speech-bubble">
      <p>Let's find the perfect food for you!</p>
      <p class="sub">Answer these questions :</p>
    </div>

    <div class="question-card">
      <div class="question-label">
        <span class="q-number">①</span>
        <span class="q-text">What's your budget?</span>
      </div>
      <div class="options-row">
        <label class="radio-option"><input type="radio" name="budget" value="under5"/><span class="radio-custom"></span>under RM 5</label>
        <label class="radio-option"><input type="radio" name="budget" value="5to10"/><span class="radio-custom"></span>RM 5 – RM 10</label>
        <label class="radio-option"><input type="radio" name="budget" value="10to15"/><span class="radio-custom"></span>RM 10 – 15</label>
        <label class="radio-option"><input type="radio" name="budget" value="above15"/><span class="radio-custom"></span>above RM 15</label>
      </div>
    </div>

    <div class="question-card">
      <div class="question-label">
        <span class="q-number">②</span>
        <span class="q-text">What type of cuisine do you feel like eating?</span>
      </div>
      <div class="options-row">
        <label class="radio-option"><input type="radio" name="cuisine" value="malay"/><span class="radio-custom"></span>Malay</label>
        <label class="radio-option"><input type="radio" name="cuisine" value="chinese"/><span class="radio-custom"></span>Chinese</label>
        <label class="radio-option"><input type="radio" name="cuisine" value="western"/><span class="radio-custom"></span>Western</label>
        <label class="radio-option"><input type="radio" name="cuisine" value="drinks"/><span class="radio-custom"></span>Drinks</label>
      </div>
    </div>

    <div class="submit-wrapper">
      <button class="submit-btn" onclick="showResult()">Submit</button>
    </div>

  </div>

  <div class="result-section" id="resultSection">

    <div class="speech-bubble">
      <p>How about <strong id="resultStallName">Rasa Shiokk</strong>?</p>
    </div>

    <div class="result-card">
      <div class="result-card-image">🍽️</div>
      <div class="result-card-info">
        <div class="result-stall-name" id="resultName">Rasa Shiokk</div>
        <div class="result-stall-cat" id="resultCat">Malaysian Cuisine</div>
        <div class="result-stall-meta">
          <span id="resultPrice">RM 4 – 20</span>
          <span class="divider">|</span>
          <span id="resultRating">⭐ 4.7</span>
        </div>
      </div>
    </div>

    <div class="result-actions">
      <a href="#" class="btn-view" id="viewStallBtn">View Stall →</a>
      <button class="btn-retry" onclick="resetQuiz()">Try Again</button>
    </div>

  </div>

</main>

<script>
  function showQuiz() {
    document.getElementById('quizSection').classList.add('visible');
    document.getElementById('triggerBtn').classList.add('active');
    document.getElementById('resultSection').classList.remove('visible');
  }

  // DYNAMIC: replace with real recommender output later
  const stallData = {
    malay:   { name: "Rasa Shiokk",  cat: "Malaysian Cuisine", price: "RM 4 – 20", rating: "⭐ 4.7", link: "{{ url_for('rasa_stall') }}" },
    chinese: { name: "Cita Rasa",    cat: "Chinese Food",      price: "RM 4 – 15", rating: "⭐ 4.3", link: "#" },
    western: { name: "Jinjja Shyok", cat: "Western Food",      price: "RM 5 – 20", rating: "⭐ 4.5", link: "#" },
    drinks:  { name: "Stall 4",      cat: "Beverages",         price: "RM 3 – 8",  rating: "⭐ 4.1", link: "#" },
  };

  function showResult() {
    const budget  = document.querySelector('input[name="budget"]:checked');
    const cuisine = document.querySelector('input[name="cuisine"]:checked');
    if (!budget || !cuisine) { alert('Please answer both questions before submitting!'); return; }
    const chosen = stallData[cuisine.value] || stallData['western'];
    document.getElementById('resultStallName').textContent = chosen.name;
    document.getElementById('resultName').textContent      = chosen.name;
    document.getElementById('resultCat').textContent       = chosen.cat;
    document.getElementById('resultPrice').textContent     = chosen.price;
    document.getElementById('resultRating').textContent    = chosen.rating;
    document.getElementById('viewStallBtn').href           = chosen.link;
    document.getElementById('quizSection').classList.remove('visible');
    document.getElementById('resultSection').classList.add('visible');
  }

  function resetQuiz() {
    document.querySelectorAll('input[type="radio"]').forEach(r => r.checked = false);
    document.getElementById('resultSection').classList.remove('visible');
    document.getElementById('quizSection').classList.add('visible');
  }
</script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# RASA SHIOKK STALL DETAIL PAGE
# ─────────────────────────────────────────────────────────────────
HTML_STALL = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rasa Shiokkk – Stall Details</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="{{ url_for('static', filename='stall.css') }}">
</head>
<body>

<nav>
  <div class="nav-logo">MMU Food Recommender System</div>
  <div class="nav-center">Stall Details</div>
  <div class="nav-right">
    <a href="{{ url_for('profile') }}">Profile</a>
    <div class="hamburger"><span></span><span></span><span></span></div>
  </div>
</nav>

<main>

  <button class="back-btn" onclick="history.back()">← Back</button>

  <div class="breadcrumb">
    <a href="{{ url_for('index') }}">Home</a>
    <span class="sep">›</span>
    <a href="#">Malaysian Cuisine</a>
    <span class="sep">›</span>
    <span class="current">Rasa Shiokkk</span>
  </div>

  <div class="stall-top">

    <div class="stall-image">
      <img src="{{ url_for('static', filename='rasa.jpg') }}" alt="Rasa Shiokkk"
           onerror="this.parentElement.innerHTML='🍛'"/>
    </div>

    <div class="stall-info">

      <div class="stall-header-row">
        <div class="stall-name">Rasa Shiokkk</div>
      </div>

      <div class="tags">
        <span class="tag">Malaysian</span>
        <span class="tag">Fusion</span>
        <span class="tag halal">Halal</span>
      </div>

      <div class="stall-category">Malaysian Cuisine · Comfort meals &amp; beverages</div>

      <div class="stall-meta">
        <span>RM 4 – 20</span>
        <span class="divider">|</span>
        <span>⭐ 4.7</span>
        <span class="review-count">(128 reviews)</span>
      </div>

      <div class="stall-location">📍 MMU Foodcourt, Starbees</div>
      <div class="stall-hours">🕙 Mon – Sun &nbsp;|&nbsp; 10:00 AM – 10:00 PM</div>

      <div class="rec-badge">
        ✨ Recommended based on your love of Malaysian food
        <span class="match-score">92% match</span>
      </div>

    </div>
  </div>

  <div class="action-buttons">
    <button class="btn btn-fav" id="favBtn" onclick="toggleFav()">
      <span id="favIcon">🤍</span> Add to Fav
      <span class="fav-count" id="favCount">· 248</span>
    </button>
    <button class="btn btn-review" onclick="document.getElementById('writeReview').scrollIntoView({behavior:'smooth'})">
      ✏️ Write a Review
    </button>
    <button class="btn btn-rate" onclick="document.getElementById('writeReview').scrollIntoView({behavior:'smooth'})">
      ⭐ Rate Us!
    </button>
  </div>

  <hr class="section-divider"/>

  <div class="section-title">🍴 Popular Menu Items</div>
  <div class="menu-grid">
    <div class="menu-item">
      <div><div class="menu-item-name">Nasi Lemak w/ Signature Chicken Chop</div><div class="menu-item-desc">Grilled, black pepper sauce</div></div>
      <div class="menu-item-price">RM 11.90</div>
    </div>
    <div class="menu-item">
      <div><div class="menu-item-name">Classic Nasi Lemak</div><div class="menu-item-desc">Sambal, egg, anchovies</div></div>
      <div class="menu-item-price">RM 5.00</div>
    </div>
    <div class="menu-item">
      <div><div class="menu-item-name">Classic Indomie</div><div class="menu-item-desc">Maggie Indomie with sambal</div></div>
      <div class="menu-item-price">RM 5.00</div>
    </div>
    <div class="menu-item">
      <div><div class="menu-item-name">Chicken Chop w/ French Fries</div><div class="menu-item-desc">With coleslaw and sauce</div></div>
      <div class="menu-item-price">RM 11.90</div>
    </div>
    <div class="menu-item">
      <div><div class="menu-item-name">Indomie w/ Curry Chicken</div><div class="menu-item-desc">Creamy curry, soft noodles</div></div>
      <div class="menu-item-price">RM 12.90</div>
    </div>
    <div class="menu-item">
      <div><div class="menu-item-name">Set Drinks</div><div class="menu-item-desc">Milo / Teh Tarik / Ice Lemon Tea</div></div>
      <div class="menu-item-price">RM 4.00</div>
    </div>
  </div>

  <hr class="section-divider"/>

  <div class="section-title">💬 User Reviews</div>
  <div class="existing-reviews" id="reviewContainer">

    <div class="review-card" style="animation-delay:0s">
      <div class="review-card-top">
        <div><div class="reviewer-name">Aisha</div><div class="review-stars">⭐⭐⭐⭐⭐</div></div>
        <div class="review-date">12 Apr 2025</div>
      </div>
      <div class="review-text">The chicken chop here is absolutely amazing! Perfectly grilled and the black pepper sauce is so flavourful. Will definitely come back again 😍</div>
    </div>

    <div class="review-card" style="animation-delay:0.1s">
      <div class="review-card-top">
        <div><div class="reviewer-name">Shar</div><div class="review-stars">⭐⭐⭐⭐</div></div>
        <div class="review-date">5 Apr 2025</div>
      </div>
      <div class="review-text">Good portion size for the price. Fish &amp; chips was crispy and fresh. Queue can be a bit long during lunch hour though.</div>
    </div>

    <div class="review-card" style="animation-delay:0.2s">
      <div class="review-card-top">
        <div><div class="reviewer-name">Shinjie</div><div class="review-stars">⭐⭐⭐⭐⭐</div></div>
        <div class="review-date">28 Mar 2025</div>
      </div>
      <div class="review-text">Best Malaysian food stall in the canteen by far. Indomie w/ curry chicken is a must-try! Friendly staff too 😊</div>
    </div>

  </div>

  <div class="write-review-box" id="writeReview">
    <h4>✍️ Leave your review</h4>
    <div class="star-picker" id="starPicker">
      <span onclick="setStars(1)">★</span>
      <span onclick="setStars(2)">★</span>
      <span onclick="setStars(3)">★</span>
      <span onclick="setStars(4)">★</span>
      <span onclick="setStars(5)">★</span>
    </div>
    <textarea class="review-textarea" id="reviewText" placeholder="Share your experience..."></textarea>
    <button class="submit-btn" onclick="submitReview()">Submit Review</button>
  </div>

  <hr class="section-divider"/>

  <div class="section-title">🔍 You Might Also Like</div>
  <div class="similar-grid">

    <div class="similar-card">
      <div class="similar-card-img">🥩</div>
      <div class="similar-card-body">
        <div class="similar-card-name">Jinjja Shyok</div>
        <div class="similar-card-meta">
          <span>Western · RM 8–18</span>
          <span class="similar-card-rating">★ 4.3</span>
        </div>
      </div>
    </div>

    <div class="similar-card">
      <div class="similar-card-img">🍝</div>
      <div class="similar-card-body">
        <div class="similar-card-name">Home Sweet Home</div>
        <div class="similar-card-meta">
          <span>Malaysian · RM 7–15</span>
          <span class="similar-card-rating">★ 4.6</span>
        </div>
      </div>
    </div>

    <div class="similar-card">
      <div class="similar-card-img">🍔</div>
      <div class="similar-card-body">
        <div class="similar-card-name">Uncle Burger</div>
        <div class="similar-card-meta">
          <span>Burgers · RM 5–14</span>
          <span class="similar-card-rating">★ 4.4</span>
        </div>
      </div>
    </div>

  </div>

</main>

<script>
  let isFav = false, favCount = 248;
  function toggleFav() {
    isFav = !isFav;
    document.getElementById('favIcon').textContent = isFav ? '❤️' : '🤍';
    document.getElementById('favCount').textContent = '· ' + (isFav ? ++favCount : --favCount);
    document.getElementById('favBtn').classList.toggle('active', isFav);
  }

  let selectedStars = 0;
  function setStars(n) {
    selectedStars = n;
    document.querySelectorAll('#starPicker span').forEach((s, i) => {
      s.classList.toggle('active', i < n);
    });
  }

  function submitReview() {
    const text = document.getElementById('reviewText').value.trim();
    if (!selectedStars) { alert('Please select a star rating!'); return; }
    if (!text) { alert('Please write something before submitting!'); return; }
    const starStr = '⭐'.repeat(selectedStars);
    const today = new Date().toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' });
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <div class="review-card-top">
        <div><div class="reviewer-name">You</div><div class="review-stars">${starStr}</div></div>
        <div class="review-date">${today}</div>
      </div>
      <div class="review-text">${text}</div>`;
    document.getElementById('reviewContainer').prepend(card);
    document.getElementById('reviewText').value = '';
    setStars(0); selectedStars = 0;
  }
</script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# PROFILE PAGE
# ─────────────────────────────────────────────────────────────────
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
            <div class="nav-right">
                <span class="profile-label">Profile</span>
                <label class="hamburger" for="menu-toggle">
                    <span></span><span></span><span></span>
                </label>
                <input type="checkbox" id="menu-toggle">
                <div class="dropdown-menu">
                    <a href="{{ url_for('index') }}">Home</a>
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
        </div>
    </header>

    <section class="profile-section">
        <div class="profile-card">
            <div class="avatar"><i class="fa fa-user"></i></div>
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

# ─────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────

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


@app.route("/suggest")
def suggest():
    logged_in = session.get("logged_in", False)
    return render_template_string(HTML_SUGGEST, logged_in=logged_in)


@app.route("/stall/rasa")
def rasa_stall():
    logged_in = session.get("logged_in", False)
    return render_template_string(HTML_STALL, logged_in=logged_in)


@app.route("/profile")
def profile():
    logged_in = session.get("logged_in", False)
    return render_template_string(HTML_PROFILE, logged_in=logged_in)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")


        return redirect(url_for("index"))

    return render_template_string(HTML_LOGIN)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        session["logged_in"] = True
        session["role"] = role
        session["name"] = name
        session["email"] = email

        return redirect(url_for("index"))

    return redirect(url_for("login") + "#signup")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)