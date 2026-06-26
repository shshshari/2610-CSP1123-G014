from flask import Flask, render_template_string, request, session, url_for, redirect
import random

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
                <span></span><span></span><span></span>
            </label>
            <input type="checkbox" id="menu-toggle">
            <div class="dropdown-menu">
                <a href="#">Favourite</a>
                <a href="#">Review</a>
                {% if session.get('role') == 'manager' %}
                    <a href="{{ url_for('feedback') }}">📋 Feedback Dashboard</a>
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
                    <input type="hidden" name="stall" value="5">
                    <button type="submit" class="fav-btn">
                        Add to Favourites <i class="fa fa-heart" style="color: {{ colors.get('5', '#ccc') }}"></i>
                    </button>
                </form>
            </div>

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

    <!-- ── FOOTER ── -->
    <footer class="site-footer">
        <div class="footer-inner">

            <div class="footer-brand">
                <span class="footer-logo">MMU Food Recommender</span>
                <p>Your campus food companion — discover, filter, and find the perfect stall.</p>
            </div>

            <div class="footer-links">
                <div class="footer-col">
                    <h4>Quick Links</h4>
                    <a href="{{ url_for('index') }}">Home</a>
                    <a href="{{ url_for('suggest') }}">What Should I Eat?</a>
                    <a href="#">Stalls</a>
                    <a href="#">Favourites</a>
                </div>
                <div class="footer-col">
                    <h4>Feedback</h4>
                    {% if session.get('role') == 'manager' %}
                        <a href="{{ url_for('feedback') }}">📋 Feedback Dashboard</a>
                    {% else %}
                        <a href="{{ url_for('feedback') }}">💬 Submit Feedback</a>
                    {% endif %}
                    {% if logged_in %}
                        <a href="{{ url_for('logout') }}">Sign Out</a>
                    {% else %}
                        <a href="{{ url_for('login') }}">Sign In / Register</a>
                    {% endif %}
                </div>
            </div>

        </div>
        <div class="footer-bottom">
            <p>© 2025 MMU Food Recommender · Group G014 · CSP1123</p>
        </div>
    </footer>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# FEEDBACK PAGE
# ─────────────────────────────────────────────────────────────────
HTML_FEEDBACK = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Feedback – MMU Food Recommender</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="{{ url_for('static', filename='feedback.css') }}"/>
</head>
<body>

<h1 class="logo">
  <img src="{{ url_for('static', filename='foodstall.png') }}" alt=""/> MMU Food Recommender
</h1>

<header>
  <div class="container">
    <nav>
      <ul class="nav-list">
        <li><a href="{{ url_for('index') }}">Home</a></li>
        <li><a href="#">Stalls</a></li>
        <li><a href="#">Favourite</a></li>
        <li><a href="#">Review</a></li>
      </ul>
    </nav>
    <div class="nav-right-group">
      <a href="{{ url_for('profile') }}" class="nav-profile">
        {% if session.get('role') == 'manager' %}Manager{% else %}Profile{% endif %}
      </a>
      <label class="hamburger" for="menu-toggle">
        <span></span><span></span><span></span>
      </label>
    </div>
    <input type="checkbox" id="menu-toggle"/>
    <div class="dropdown-menu">
      <a href="{{ url_for('index') }}">Home</a>
      <a href="#">Favourite</a>
      <a href="{{ url_for('profile') }}">Profile</a>
      {% if logged_in %}
        <a href="{{ url_for('logout') }}">Sign Out</a>
      {% else %}
        <a href="{{ url_for('login') }}">Sign In</a>
      {% endif %}
    </div>
  </div>
</header>

<main>

  <button class="back-btn" onclick="history.back()">← Back</button>

  {% if session.get('role') == 'manager' %}

  <div class="manager-wrapper">

    <div class="manager-header">
      <div>
        <h2>📋 Feedback Dashboard</h2>
        <p>Review all user feedback submitted for the MMU Food Recommender</p>
      </div>
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-num" id="totalCount">5</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat-card green">
          <div class="stat-num" id="resolvedCount">2</div>
          <div class="stat-label">Resolved</div>
        </div>
        <div class="stat-card orange">
          <div class="stat-num" id="pendingCount">3</div>
          <div class="stat-label">Pending</div>
        </div>
      </div>
    </div>

    <div class="manager-filters">
      <input type="text" class="filter-search" id="filterInput"
             placeholder="🔍 Search by name or keyword..." oninput="filterCards()"/>
      <select class="filter-select" id="filterCat" onchange="filterCards()">
        <option value="">All Categories</option>
        <option value="recommendation">Recommendation Quality</option>
        <option value="ui">Website Design / UI</option>
        <option value="stall">Stall Information</option>
        <option value="bug">Bug / Technical Issue</option>
        <option value="other">Other</option>
      </select>
      <select class="filter-select" id="filterStatus" onchange="filterCards()">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="resolved">Resolved</option>
      </select>
    </div>

    <!-- DYNAMIC: replace dummy cards with DB data later -->
    <div class="feedback-list" id="feedbackList">

      <div class="fb-card" data-cat="recommendation" data-status="pending">
        <div class="fb-card-top">
          <div class="fb-user">
            <div class="fb-avatar">A</div>
            <div><div class="fb-name">Aisha Razak</div><div class="fb-email">aisha@student.mmu.edu.my</div></div>
          </div>
          <div class="fb-meta">
            <span class="fb-cat">Recommendation Quality</span>
            <span class="fb-stars">⭐⭐⭐⭐⭐</span>
            <span class="fb-date">12 Apr 2025</span>
            <span class="fb-status pending">Pending</span>
          </div>
        </div>
        <div class="fb-message">"The recommendations are really accurate! Would be great if there were more filter options though."</div>
        <div class="fb-actions">
          <button class="btn-resolve" onclick="resolveCard(this)">✅ Mark Resolved</button>
          <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>
        </div>
      </div>

      <div class="fb-card" data-cat="bug" data-status="pending">
        <div class="fb-card-top">
          <div class="fb-user">
            <div class="fb-avatar">H</div>
            <div><div class="fb-name">Haziq Mahmud</div><div class="fb-email">haziq@student.mmu.edu.my</div></div>
          </div>
          <div class="fb-meta">
            <span class="fb-cat bug">Bug / Technical Issue</span>
            <span class="fb-stars">⭐⭐⭐</span>
            <span class="fb-date">10 Apr 2025</span>
            <span class="fb-status pending">Pending</span>
          </div>
        </div>
        <div class="fb-message">"The favourite button sometimes doesn't save when I refresh the page."</div>
        <div class="fb-actions">
          <button class="btn-resolve" onclick="resolveCard(this)">✅ Mark Resolved</button>
          <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>
        </div>
      </div>

      <div class="fb-card" data-cat="ui" data-status="resolved">
        <div class="fb-card-top">
          <div class="fb-user">
            <div class="fb-avatar">W</div>
            <div><div class="fb-name">Wei Ling Tan</div><div class="fb-email">weiling@student.mmu.edu.my</div></div>
          </div>
          <div class="fb-meta">
            <span class="fb-cat ui">Website Design / UI</span>
            <span class="fb-stars">⭐⭐⭐⭐</span>
            <span class="fb-date">8 Apr 2025</span>
            <span class="fb-status resolved">Resolved</span>
          </div>
        </div>
        <div class="fb-message">"Love the design overall! Maybe add dark mode in the future? 😊"</div>
        <div class="fb-actions">
          <button class="btn-unresolve" onclick="unresolveCard(this)">↩ Mark Pending</button>
          <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>
        </div>
      </div>

      <div class="fb-card" data-cat="stall" data-status="pending">
        <div class="fb-card-top">
          <div class="fb-user">
            <div class="fb-avatar">S</div>
            <div><div class="fb-name">Shar Lim</div><div class="fb-email">shar@student.mmu.edu.my</div></div>
          </div>
          <div class="fb-meta">
            <span class="fb-cat stall">Stall Information</span>
            <span class="fb-stars">⭐⭐⭐⭐</span>
            <span class="fb-date">5 Apr 2025</span>
            <span class="fb-status pending">Pending</span>
          </div>
        </div>
        <div class="fb-message">"The opening hours for Cita Rasa seem wrong — they actually close at 3pm, not 5pm."</div>
        <div class="fb-actions">
          <button class="btn-resolve" onclick="resolveCard(this)">✅ Mark Resolved</button>
          <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>
        </div>
      </div>

      <div class="fb-card" data-cat="recommendation" data-status="resolved">
        <div class="fb-card-top">
          <div class="fb-user">
            <div class="fb-avatar">R</div>
            <div><div class="fb-name">Rajan Kumar</div><div class="fb-email">rajan@student.mmu.edu.my</div></div>
          </div>
          <div class="fb-meta">
            <span class="fb-cat">Recommendation Quality</span>
            <span class="fb-stars">⭐⭐⭐⭐⭐</span>
            <span class="fb-date">2 Apr 2025</span>
            <span class="fb-status resolved">Resolved</span>
          </div>
        </div>
        <div class="fb-message">"The What Should I Eat feature is genius! Keep up the great work team 👍"</div>
        <div class="fb-actions">
          <button class="btn-unresolve" onclick="unresolveCard(this)">↩ Mark Pending</button>
          <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>
        </div>
      </div>

    </div>

    <div class="no-feedback" id="noFeedback">
      <div style="font-size:2.5rem">📭</div>
      <p>No feedback found matching your filters.</p>
    </div>

  </div>

  {% else %}

  <div class="feedback-wrapper">

    <div class="feedback-header">
      <div class="feedback-icon">💬</div>
      <h2>Share Your Feedback</h2>
      <p>Help us improve the MMU Food Recommender. We read every response!</p>
    </div>

    <form class="feedback-form" id="feedbackForm" onsubmit="submitFeedback(event)">

      <div class="form-row">
        <div class="form-group">
          <label for="fbName">Your Name</label>
          <input type="text" id="fbName" name="name"
                 placeholder="e.g. Aisha Binti Razak"
                 value="{{ session.get('name', '') }}" required/>
        </div>
        <div class="form-group">
          <label for="fbEmail">Email Address</label>
          <input type="email" id="fbEmail" name="email"
                 placeholder="e.g. aisha@student.mmu.edu.my"
                 value="{{ session.get('email', '') }}" required/>
        </div>
      </div>

      <div class="form-group">
        <label for="fbCategory">Feedback Category</label>
        <select id="fbCategory" name="category" required>
          <option value="">Select a category</option>
          <option value="recommendation">Recommendation Quality</option>
          <option value="ui">Website Design / UI</option>
          <option value="stall">Stall Information</option>
          <option value="bug">Bug / Technical Issue</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label>Overall Experience</label>
        <div class="star-rating" id="starRating">
          <span onclick="setRating(1)">★</span>
          <span onclick="setRating(2)">★</span>
          <span onclick="setRating(3)">★</span>
          <span onclick="setRating(4)">★</span>
          <span onclick="setRating(5)">★</span>
        </div>
        <input type="hidden" id="ratingVal" name="rating"/>
      </div>

      <div class="form-group">
        <label for="fbMessage">Your Feedback</label>
        <textarea id="fbMessage" name="message" rows="5"
                  placeholder="Tell us what you think — what's working well, what could be better..." required></textarea>
      </div>

      <button type="submit" class="submit-btn">
        <i class="fa fa-paper-plane"></i> Submit Feedback
      </button>

    </form>

    <div class="success-msg" id="successMsg">
      <div class="success-icon">✅</div>
      <h3>Thank you for your feedback!</h3>
      <p>We really appreciate you taking the time to share your thoughts.</p>
      <a href="{{ url_for('index') }}" class="back-home-btn">← Back to Home</a>
    </div>

  </div>

  {% endif %}

</main>

<footer>
  <p>© 2025 MMU Food Recommender &nbsp;·&nbsp; Group G014 &nbsp;·&nbsp; CSP1123</p>
</footer>

<script>
  let selectedRating = 0;
  function setRating(n) {
    selectedRating = n;
    document.getElementById('ratingVal').value = n;
    document.querySelectorAll('#starRating span').forEach((s, i) => {
      s.classList.toggle('active', i < n);
    });
  }
  function submitFeedback(e) {
    e.preventDefault();
    if (!selectedRating) { alert('Please select a star rating!'); return; }
    // DYNAMIC: POST to backend here later
    document.getElementById('feedbackForm').style.display = 'none';
    document.getElementById('successMsg').style.display = 'flex';
  }
  function updateStats() {
    const all      = document.querySelectorAll('.fb-card');
    const resolved = document.querySelectorAll('.fb-card[data-status="resolved"]');
    const pending  = document.querySelectorAll('.fb-card[data-status="pending"]');
    if (document.getElementById('totalCount'))    document.getElementById('totalCount').textContent    = all.length;
    if (document.getElementById('resolvedCount')) document.getElementById('resolvedCount').textContent = resolved.length;
    if (document.getElementById('pendingCount'))  document.getElementById('pendingCount').textContent  = pending.length;
  }
  function resolveCard(btn) {
    const card = btn.closest('.fb-card');
    card.dataset.status = 'resolved';
    card.querySelector('.fb-status').textContent = 'Resolved';
    card.querySelector('.fb-status').className = 'fb-status resolved';
    card.querySelector('.fb-actions').innerHTML = `
      <button class="btn-unresolve" onclick="unresolveCard(this)">↩ Mark Pending</button>
      <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>`;
    updateStats();
  }
  function unresolveCard(btn) {
    const card = btn.closest('.fb-card');
    card.dataset.status = 'pending';
    card.querySelector('.fb-status').textContent = 'Pending';
    card.querySelector('.fb-status').className = 'fb-status pending';
    card.querySelector('.fb-actions').innerHTML = `
      <button class="btn-resolve" onclick="resolveCard(this)">✅ Mark Resolved</button>
      <button class="btn-delete" onclick="deleteCard(this)">🗑 Delete</button>`;
    updateStats();
  }
  function deleteCard(btn) {
    if (!confirm('Delete this feedback?')) return;
    const card = btn.closest('.fb-card');
    card.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => { card.remove(); updateStats(); filterCards(); }, 300);
  }
  function filterCards() {
    const query  = document.getElementById('filterInput') ? document.getElementById('filterInput').value.toLowerCase() : '';
    const cat    = document.getElementById('filterCat') ? document.getElementById('filterCat').value : '';
    const status = document.getElementById('filterStatus') ? document.getElementById('filterStatus').value : '';
    const cards  = document.querySelectorAll('.fb-card');
    let visible  = 0;
    cards.forEach(card => {
      const matchText = !query || card.textContent.toLowerCase().includes(query);
      const matchCat  = !cat || card.dataset.cat === cat;
      const matchStat = !status || card.dataset.status === status;
      card.style.display = (matchText && matchCat && matchStat) ? 'block' : 'none';
      if (matchText && matchCat && matchStat) visible++;
    });
    const noFb = document.getElementById('noFeedback');
    if (noFb) noFb.style.display = visible === 0 ? 'flex' : 'none';
  }
  updateStats();
</script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# LOGIN PAGE  (updated: "Forgot your password?" now links to route)
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

        <div class="form-container sign-up">
            <form method="POST" action="{{ url_for('register') }}">
                <h1>Create Account</h1>
                <span>or use your email</span>
                <input type="text" name="name" placeholder="Name" required/>
                <input type="email" name="email" placeholder="Email" required/>
                <input type="password" name="password" placeholder="Password" required/>
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

        <div class="form-container sign-in">
            <form method="POST" action="{{ url_for('login') }}">
                <h1>Sign In</h1>
                <span>or use your email and password</span>
                <input type="email" name="email" placeholder="Email" required/>
                <input type="password" name="password" placeholder="Password" required/>
                <a href="{{ url_for('forgot_password') }}">Forgot your password?</a>
                <button type="submit">Sign In</button>
            </form>
        </div>

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

    <a href="{{ url_for('index') }}" class="back-home">← Back </a>

    <script>
        const container      = document.getElementById('container');
        const registerToggle = document.getElementById('registerToggle');
        const loginToggle    = document.getElementById('loginToggle');
        registerToggle.addEventListener('click', () => container.classList.add('active'));
        loginToggle.addEventListener('click',    () => container.classList.remove('active'));
        if (window.location.hash === '#signup') container.classList.add('active');
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# FORGOT PASSWORD 
# ─────────────────────────────────────────────────────────────────
HTML_FORGOT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Forgot Password – MMU Food Recommender</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Nunito', sans-serif;
            background: #fdf6ec;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        /* ── top logo bar ── */
        .top-bar {
            position: fixed;
            top: 0; left: 0; right: 0;
            background: #1c4273;
            padding: 14px 32px;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 100;
        }
        .top-bar .site-name {
            color: #fff;
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 0.3px;
            text-decoration: none;
        }

        /* ── card ── */
        .card {
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(28,66,115,0.12);
            padding: 48px 44px;
            width: 100%;
            max-width: 440px;
            text-align: center;
            margin-top: 56px;
        }

        .icon-circle {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #f97316, #fb923c);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 24px;
            box-shadow: 0 4px 16px rgba(249,115,22,0.3);
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1c4273;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 0.92rem;
            color: #7a8599;
            margin-bottom: 32px;
            line-height: 1.5;
        }

        /* ── steps indicator ── */
        .steps {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            margin-bottom: 32px;
        }
        .step-dot {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e5e9f2;
            color: #aab0c0;
            font-size: 0.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .step-dot.active {
            background: #1c4273;
            color: #fff;
        }
        .step-dot.done {
            background: #f97316;
            color: #fff;
        }
        .step-line {
            width: 48px;
            height: 3px;
            background: #e5e9f2;
        }
        .step-line.done { background: #f97316; }

        /* ── form ── */
        label {
            display: block;
            text-align: left;
            font-size: 0.85rem;
            font-weight: 700;
            color: #1c4273;
            margin-bottom: 6px;
        }
        input[type="email"] {
            width: 100%;
            padding: 13px 16px;
            border: 2px solid #e5e9f2;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-size: 0.95rem;
            color: #2d3748;
            outline: none;
            transition: border-color 0.2s;
            margin-bottom: 24px;
        }
        input[type="email"]:focus { border-color: #1c4273; }

        .btn-primary {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #1c4273, #2a5ca8);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-size: 1rem;
            font-weight: 800;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            letter-spacing: 0.3px;
        }
        .btn-primary:hover { opacity: 0.92; }
        .btn-primary:active { transform: scale(0.98); }

        .back-link {
            display: inline-block;
            margin-top: 20px;
            font-size: 0.88rem;
            color: #7a8599;
            text-decoration: none;
            transition: color 0.2s;
        }
        .back-link:hover { color: #1c4273; }

        /* ── flash message ── */
        .flash {
            background: #fef2f2;
            border: 1.5px solid #fca5a5;
            color: #b91c1c;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.88rem;
            margin-bottom: 18px;
            text-align: left;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="{{ url_for('index') }}" class="site-name">🍽️ MMU Food Recommender</a>
    </div>

    <div class="card">

        <div class="icon-circle">🔐</div>
        <h1>Forgot Password?</h1>
        <p class="subtitle">No worries! Enter your registered email and we'll send you a verification code.</p>

        <!-- Step indicator: 1 of 3 -->
        <div class="steps">
            <div class="step-dot active">1</div>
            <div class="step-line"></div>
            <div class="step-dot">2</div>
            <div class="step-line"></div>
            <div class="step-dot">3</div>
        </div>

        {% if error %}
        <div class="flash">{{ error }}</div>
        {% endif %}

        <form method="POST" action="{{ url_for('forgot_password') }}">
            <label for="email">Email Address</label>
            <input type="email" id="email" name="email"
                   placeholder="e.g. aisha@student.mmu.edu.my"
                   value="{{ prefill or '' }}" required/>
            <button type="submit" class="btn-primary">Send Verification Code →</button>
        </form>

        <a href="{{ url_for('login') }}" class="back-link">← Back to Sign In</a>

    </div>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# VERIFY CODE — Step 2: Enter 6-digit code
# ─────────────────────────────────────────────────────────────────
HTML_VERIFY = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Verify Code – MMU Food Recommender</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Nunito', sans-serif;
            background: #fdf6ec;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .top-bar {
            position: fixed;
            top: 0; left: 0; right: 0;
            background: #1c4273;
            padding: 14px 32px;
            display: flex;
            align-items: center;
            z-index: 100;
        }
        .top-bar .site-name {
            color: #fff;
            font-size: 1.1rem;
            font-weight: 800;
            text-decoration: none;
        }

        .card {
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(28,66,115,0.12);
            padding: 48px 44px;
            width: 100%;
            max-width: 440px;
            text-align: center;
            margin-top: 56px;
        }

        .icon-circle {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #f97316, #fb923c);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 24px;
            box-shadow: 0 4px 16px rgba(249,115,22,0.3);
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1c4273;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 0.92rem;
            color: #7a8599;
            margin-bottom: 8px;
            line-height: 1.5;
        }
        .email-highlight {
            font-weight: 700;
            color: #f97316;
        }

        .steps {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            margin: 24px 0 32px;
        }
        .step-dot {
            width: 30px; height: 30px;
            border-radius: 50%;
            background: #e5e9f2;
            color: #aab0c0;
            font-size: 0.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .step-dot.active { background: #1c4273; color: #fff; }
        .step-dot.done   { background: #f97316; color: #fff; }
        .step-line       { width: 48px; height: 3px; background: #e5e9f2; }
        .step-line.done  { background: #f97316; }

        /* 6-box code input */
        .code-inputs {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 28px;
        }
        .code-inputs input {
            width: 48px;
            height: 56px;
            border: 2px solid #e5e9f2;
            border-radius: 10px;
            text-align: center;
            font-size: 1.4rem;
            font-weight: 800;
            font-family: 'Nunito', sans-serif;
            color: #1c4273;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .code-inputs input:focus {
            border-color: #1c4273;
            box-shadow: 0 0 0 3px rgba(28,66,115,0.1);
        }

        /* hidden combined field for submission */
        input[name="code"] { display: none; }

        .btn-primary {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #1c4273, #2a5ca8);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-size: 1rem;
            font-weight: 800;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
        }
        .btn-primary:hover { opacity: 0.92; }
        .btn-primary:active { transform: scale(0.98); }

        .resend-row {
            margin-top: 18px;
            font-size: 0.88rem;
            color: #7a8599;
        }
        .resend-row a {
            color: #f97316;
            font-weight: 700;
            text-decoration: none;
        }
        .resend-row a:hover { text-decoration: underline; }

        .back-link {
            display: inline-block;
            margin-top: 14px;
            font-size: 0.88rem;
            color: #7a8599;
            text-decoration: none;
        }
        .back-link:hover { color: #1c4273; }

        .flash {
            background: #fef2f2;
            border: 1.5px solid #fca5a5;
            color: #b91c1c;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.88rem;
            margin-bottom: 18px;
            text-align: left;
        }

        /* dev helper – shows dummy code in a soft pill */
        .dev-hint {
            background: #f0fdf4;
            border: 1.5px solid #86efac;
            color: #166534;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 0.82rem;
            margin-bottom: 20px;
        }
        /* DYNAMIC: remove .dev-hint block once real email sending is wired up */
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="{{ url_for('index') }}" class="site-name">🍽️ MMU Food Recommender</a>
    </div>

    <div class="card">

        <div class="icon-circle">📩</div>
        <h1>Check Your Email</h1>
        <p class="subtitle">We sent a 6-digit code to<br><span class="email-highlight">{{ email }}</span></p>

        <!-- Step indicator: 2 of 3 -->
        <div class="steps">
            <div class="step-dot done">✓</div>
            <div class="step-line done"></div>
            <div class="step-dot active">2</div>
            <div class="step-line"></div>
            <div class="step-dot">3</div>
        </div>

        {% if error %}
        <div class="flash">{{ error }}</div>
        {% endif %}

        <!-- DYNAMIC: remove this dev hint once real email is wired up -->
        <div class="dev-hint">🛠 Dev mode — your code is: <strong>{{ dev_code }}</strong></div>

        <form method="POST" action="{{ url_for('verify_code') }}" id="codeForm">
            <div class="code-inputs" id="codeBoxes">
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
                <input type="text" maxlength="1" inputmode="numeric" pattern="[0-9]" autocomplete="off"/>
            </div>
            <input type="hidden" name="code" id="combinedCode"/>
            <button type="submit" class="btn-primary">Verify Code →</button>
        </form>

        <div class="resend-row">
            Didn't receive it? <a href="{{ url_for('forgot_password_resend') }}">Resend code</a>
        </div>
        <br>
        <a href="{{ url_for('forgot_password') }}" class="back-link">← Change email</a>

    </div>

    <script>
        const boxes = document.querySelectorAll('#codeBoxes input');

        boxes.forEach((box, i) => {
            box.addEventListener('input', () => {
                // only allow digits
                box.value = box.value.replace(/\D/g, '');
                if (box.value && i < boxes.length - 1) boxes[i + 1].focus();
            });
            box.addEventListener('keydown', e => {
                if (e.key === 'Backspace' && !box.value && i > 0) boxes[i - 1].focus();
            });
            // allow paste on any box
            box.addEventListener('paste', e => {
                e.preventDefault();
                const digits = (e.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, 6);
                digits.split('').forEach((d, j) => {
                    if (boxes[j]) boxes[j].value = d;
                });
                const last = Math.min(digits.length, boxes.length - 1);
                boxes[last].focus();
            });
        });

        document.getElementById('codeForm').addEventListener('submit', () => {
            document.getElementById('combinedCode').value =
                Array.from(boxes).map(b => b.value).join('');
        });
    </script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# RESET PASSWORD — Step 3: Set new password
# ─────────────────────────────────────────────────────────────────
HTML_RESET = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reset Password – MMU Food Recommender</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Nunito', sans-serif;
            background: #fdf6ec;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .top-bar {
            position: fixed;
            top: 0; left: 0; right: 0;
            background: #1c4273;
            padding: 14px 32px;
            display: flex;
            align-items: center;
            z-index: 100;
        }
        .top-bar .site-name {
            color: #fff;
            font-size: 1.1rem;
            font-weight: 800;
            text-decoration: none;
        }

        .card {
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(28,66,115,0.12);
            padding: 48px 44px;
            width: 100%;
            max-width: 440px;
            text-align: center;
            margin-top: 56px;
        }

        .icon-circle {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #f97316, #fb923c);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 24px;
            box-shadow: 0 4px 16px rgba(249,115,22,0.3);
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1c4273;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 0.92rem;
            color: #7a8599;
            margin-bottom: 8px;
            line-height: 1.5;
        }

        .steps {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            margin: 24px 0 32px;
        }
        .step-dot {
            width: 30px; height: 30px;
            border-radius: 50%;
            background: #e5e9f2;
            color: #aab0c0;
            font-size: 0.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .step-dot.active { background: #1c4273; color: #fff; }
        .step-dot.done   { background: #f97316; color: #fff; }
        .step-line       { width: 48px; height: 3px; background: #e5e9f2; }
        .step-line.done  { background: #f97316; }

        label {
            display: block;
            text-align: left;
            font-size: 0.85rem;
            font-weight: 700;
            color: #1c4273;
            margin-bottom: 6px;
        }
        .input-wrap {
            position: relative;
            margin-bottom: 18px;
        }
        .input-wrap input {
            width: 100%;
            padding: 13px 44px 13px 16px;
            border: 2px solid #e5e9f2;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-size: 0.95rem;
            color: #2d3748;
            outline: none;
            transition: border-color 0.2s;
        }
        .input-wrap input:focus { border-color: #1c4273; }
        .toggle-eye {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 1rem;
            color: #aab0c0;
            user-select: none;
        }

        /* password strength bar */
        .strength-bar-wrap {
            height: 6px;
            background: #e5e9f2;
            border-radius: 4px;
            margin: -12px 0 18px;
            overflow: hidden;
        }
        .strength-bar {
            height: 100%;
            width: 0%;
            border-radius: 4px;
            transition: width 0.3s, background 0.3s;
        }
        .strength-label {
            text-align: left;
            font-size: 0.78rem;
            color: #aab0c0;
            margin-top: -14px;
            margin-bottom: 18px;
        }

        .requirements {
            background: #f8faff;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 24px;
            text-align: left;
        }
        .req-item {
            font-size: 0.8rem;
            color: #aab0c0;
            margin: 4px 0;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: color 0.2s;
        }
        .req-item.met { color: #22c55e; }
        .req-item .dot { font-size: 0.6rem; }

        .btn-primary {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #1c4273, #2a5ca8);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-size: 1rem;
            font-weight: 800;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
        }
        .btn-primary:hover { opacity: 0.92; }
        .btn-primary:active { transform: scale(0.98); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

        .flash {
            background: #fef2f2;
            border: 1.5px solid #fca5a5;
            color: #b91c1c;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.88rem;
            margin-bottom: 18px;
            text-align: left;
        }

        /* success state */
        .success-card { display: none; text-align: center; }
        .success-card .big-icon { font-size: 3.5rem; margin-bottom: 16px; }
        .success-card h2 { font-size: 1.4rem; color: #1c4273; font-weight: 800; margin-bottom: 8px; }
        .success-card p { color: #7a8599; font-size: 0.9rem; margin-bottom: 28px; }
        .btn-go-login {
            display: inline-block;
            padding: 13px 32px;
            background: linear-gradient(135deg, #f97316, #fb923c);
            color: #fff;
            border-radius: 10px;
            font-family: 'Nunito', sans-serif;
            font-weight: 800;
            font-size: 0.95rem;
            text-decoration: none;
            transition: opacity 0.2s;
        }
        .btn-go-login:hover { opacity: 0.88; }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="{{ url_for('index') }}" class="site-name">🍽️ MMU Food Recommender</a>
    </div>

    <div class="card">

        <div id="formSection">
            <div class="icon-circle">🔑</div>
            <h1>Set New Password</h1>
            <p class="subtitle">Almost done! Create a strong new password for your account.</p>

            <!-- Step indicator: 3 of 3 -->
            <div class="steps">
                <div class="step-dot done">✓</div>
                <div class="step-line done"></div>
                <div class="step-dot done">✓</div>
                <div class="step-line done"></div>
                <div class="step-dot active">3</div>
            </div>

            {% if error %}
            <div class="flash">{{ error }}</div>
            {% endif %}

            <form method="POST" action="{{ url_for('reset_password') }}" id="resetForm">

                <label for="newpw">New Password</label>
                <div class="input-wrap">
                    <input type="password" id="newpw" name="password"
                           placeholder="Enter new password" required
                           oninput="checkStrength(this.value)"/>
                    <span class="toggle-eye" onclick="togglePw('newpw', this)">👁</span>
                </div>
                <div class="strength-bar-wrap">
                    <div class="strength-bar" id="strengthBar"></div>
                </div>
                <div class="strength-label" id="strengthLabel">Enter a password</div>

                <div class="requirements" id="reqs">
                    <div class="req-item" id="req-len"><span class="dot">●</span> At least 8 characters</div>
                    <div class="req-item" id="req-upper"><span class="dot">●</span> One uppercase letter</div>
                    <div class="req-item" id="req-num"><span class="dot">●</span> One number</div>
                    <div class="req-item" id="req-special"><span class="dot">●</span> One special character (!@#$…)</div>
                </div>

                <label for="confirmpw">Confirm Password</label>
                <div class="input-wrap">
                    <input type="password" id="confirmpw" name="confirm_password"
                           placeholder="Re-enter new password" required/>
                    <span class="toggle-eye" onclick="togglePw('confirmpw', this)">👁</span>
                </div>

                <button type="submit" class="btn-primary" id="submitBtn">Reset Password ✓</button>
            </form>
        </div>

        <!-- shown on successful reset -->
        <div class="success-card" id="successSection">
            <div class="big-icon">🎉</div>
            <h2>Password Reset!</h2>
            <p>Your password has been updated successfully.<br>You can now sign in with your new password.</p>
            <a href="{{ url_for('login') }}" class="btn-go-login">Go to Sign In →</a>
        </div>

    </div>

    <script>
        function togglePw(id, el) {
            const inp = document.getElementById(id);
            inp.type = inp.type === 'password' ? 'text' : 'password';
            el.textContent = inp.type === 'password' ? '👁' : '🙈';
        }

        function checkStrength(val) {
            const bar   = document.getElementById('strengthBar');
            const label = document.getElementById('strengthLabel');
            const len     = val.length >= 8;
            const upper   = /[A-Z]/.test(val);
            const num     = /[0-9]/.test(val);
            const special = /[^A-Za-z0-9]/.test(val);

            setReq('req-len',     len);
            setReq('req-upper',   upper);
            setReq('req-num',     num);
            setReq('req-special', special);

            const score = [len, upper, num, special].filter(Boolean).length;
            const configs = [
                { w: '0%',   bg: '#e5e9f2', txt: 'Enter a password' },
                { w: '25%',  bg: '#ef4444', txt: 'Weak' },
                { w: '50%',  bg: '#f97316', txt: 'Fair' },
                { w: '75%',  bg: '#eab308', txt: 'Good' },
                { w: '100%', bg: '#22c55e', txt: 'Strong 💪' },
            ];
            const cfg = configs[score];
            bar.style.width      = cfg.w;
            bar.style.background = cfg.bg;
            label.textContent    = val ? cfg.txt : 'Enter a password';
        }

        function setReq(id, met) {
            document.getElementById(id).classList.toggle('met', met);
        }

        document.getElementById('resetForm').addEventListener('submit', function(e) {
            const pw  = document.getElementById('newpw').value;
            const cpw = document.getElementById('confirmpw').value;
            if (pw !== cpw) {
                e.preventDefault();
                alert('Passwords do not match. Please try again.');
                return;
            }
            // DYNAMIC: POST to backend for real DB password update later
            // For now, show success UI immediately
            e.preventDefault();
            document.getElementById('formSection').style.display = 'none';
            document.getElementById('successSection').style.display = 'block';
        });
    </script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────
# WHAT SHOULD I EAT
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
      <span class="trigger-icon">?</span> What Should I Eat?
    </button>
  </div>
  <div class="quiz-section" id="quizSection">
    <div class="speech-bubble">
      <p>Let's find the perfect food for you!</p>
      <p class="sub">Answer these questions :</p>
    </div>
    <div class="question-card">
      <div class="question-label"><span class="q-number">①</span><span class="q-text">What's your budget?</span></div>
      <div class="options-row">
        <label class="radio-option"><input type="radio" name="budget" value="under5"/><span class="radio-custom"></span>under RM 5</label>
        <label class="radio-option"><input type="radio" name="budget" value="5to10"/><span class="radio-custom"></span>RM 5 – RM 10</label>
        <label class="radio-option"><input type="radio" name="budget" value="10to15"/><span class="radio-custom"></span>RM 10 – 15</label>
        <label class="radio-option"><input type="radio" name="budget" value="above15"/><span class="radio-custom"></span>above RM 15</label>
      </div>
    </div>
    <div class="question-card">
      <div class="question-label"><span class="q-number">②</span><span class="q-text">What type of cuisine do you feel like eating?</span></div>
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
    <a href="{{ url_for('index') }}">Home</a><span class="sep">›</span>
    <a href="#">Malaysian Cuisine</a><span class="sep">›</span>
    <span class="current">Rasa Shiokkk</span>
  </div>
  <div class="stall-top">
    <div class="stall-image">
      <img src="{{ url_for('static', filename='rasa.jpg') }}" alt="Rasa Shiokkk" onerror="this.parentElement.innerHTML='🍛'"/>
    </div>
    <div class="stall-info">
      <div class="stall-header-row"><div class="stall-name">Rasa Shiokkk</div></div>
      <div class="tags">
        <span class="tag">Malaysian</span><span class="tag">Fusion</span><span class="tag halal">Halal</span>
      </div>
      <div class="stall-category">Malaysian Cuisine · Comfort meals &amp; beverages</div>
      <div class="stall-meta">
        <span>RM 4 – 20</span><span class="divider">|</span>
        <span>⭐ 4.7</span><span class="review-count">(128 reviews)</span>
      </div>
      <div class="stall-location">📍 MMU Foodcourt, Starbees</div>
      <div class="stall-hours">🕙 Mon – Sun &nbsp;|&nbsp; 10:00 AM – 10:00 PM</div>
      <div class="rec-badge">✨ Recommended based on your love of Malaysian food<span class="match-score">92% match</span></div>
    </div>
  </div>
  <div class="action-buttons">
    <button class="btn btn-fav" id="favBtn" onclick="toggleFav()">
      <span id="favIcon">🤍</span> Add to Fav <span class="fav-count" id="favCount">· 248</span>
    </button>
    <button class="btn btn-review" onclick="document.getElementById('writeReview').scrollIntoView({behavior:'smooth'})">✏️ Write a Review</button>
    <button class="btn btn-rate" onclick="document.getElementById('writeReview').scrollIntoView({behavior:'smooth'})">⭐ Rate Us!</button>
  </div>
  <hr class="section-divider"/>
  <div class="section-title">🍴 Popular Menu Items</div>
  <div class="menu-grid">
    <div class="menu-item"><div><div class="menu-item-name">Nasi Lemak w/ Signature Chicken Chop</div><div class="menu-item-desc">Grilled, black pepper sauce</div></div><div class="menu-item-price">RM 11.90</div></div>
    <div class="menu-item"><div><div class="menu-item-name">Classic Nasi Lemak</div><div class="menu-item-desc">Sambal, egg, anchovies</div></div><div class="menu-item-price">RM 5.00</div></div>
    <div class="menu-item"><div><div class="menu-item-name">Classic Indomie</div><div class="menu-item-desc">Maggie Indomie with sambal</div></div><div class="menu-item-price">RM 5.00</div></div>
    <div class="menu-item"><div><div class="menu-item-name">Chicken Chop w/ French Fries</div><div class="menu-item-desc">With coleslaw and sauce</div></div><div class="menu-item-price">RM 11.90</div></div>
    <div class="menu-item"><div><div class="menu-item-name">Indomie w/ Curry Chicken</div><div class="menu-item-desc">Creamy curry, soft noodles</div></div><div class="menu-item-price">RM 12.90</div></div>
    <div class="menu-item"><div><div class="menu-item-name">Set Drinks</div><div class="menu-item-desc">Milo / Teh Tarik / Ice Lemon Tea</div></div><div class="menu-item-price">RM 4.00</div></div>
  </div>
  <hr class="section-divider"/>
  <div class="section-title">💬 User Reviews</div>
  <div class="existing-reviews" id="reviewContainer">
    <div class="review-card"><div class="review-card-top"><div><div class="reviewer-name">Aisha</div><div class="review-stars">⭐⭐⭐⭐⭐</div></div><div class="review-date">12 Apr 2025</div></div><div class="review-text">The chicken chop here is absolutely amazing! Will definitely come back again 😍</div></div>
    <div class="review-card"><div class="review-card-top"><div><div class="reviewer-name">Shar</div><div class="review-stars">⭐⭐⭐⭐</div></div><div class="review-date">5 Apr 2025</div></div><div class="review-text">Good portion size for the price. Queue can be a bit long during lunch hour though.</div></div>
    <div class="review-card"><div class="review-card-top"><div><div class="reviewer-name">Shinjie</div><div class="review-stars">⭐⭐⭐⭐⭐</div></div><div class="review-date">28 Mar 2025</div></div><div class="review-text">Best Malaysian food stall in the canteen by far. Friendly staff too 😊</div></div>
  </div>
  <div class="write-review-box" id="writeReview">
    <h4>✍️ Leave your review</h4>
    <div class="star-picker" id="starPicker">
      <span onclick="setStars(1)">★</span><span onclick="setStars(2)">★</span>
      <span onclick="setStars(3)">★</span><span onclick="setStars(4)">★</span><span onclick="setStars(5)">★</span>
    </div>
    <textarea class="review-textarea" id="reviewText" placeholder="Share your experience..."></textarea>
    <button class="submit-btn" onclick="submitReview()">Submit Review</button>
  </div>
  <hr class="section-divider"/>
  <div class="section-title">🔍 You Might Also Like</div>
  <div class="similar-grid">
    <div class="similar-card"><div class="similar-card-img">🥩</div><div class="similar-card-body"><div class="similar-card-name">Jinjja Shyok</div><div class="similar-card-meta"><span>Western · RM 8–18</span><span class="similar-card-rating">★ 4.3</span></div></div></div>
    <div class="similar-card"><div class="similar-card-img">🍝</div><div class="similar-card-body"><div class="similar-card-name">Home Sweet Home</div><div class="similar-card-meta"><span>Malaysian · RM 7–15</span><span class="similar-card-rating">★ 4.6</span></div></div></div>
    <div class="similar-card"><div class="similar-card-img">🍔</div><div class="similar-card-body"><div class="similar-card-name">Uncle Burger</div><div class="similar-card-meta"><span>Burgers · RM 5–14</span><span class="similar-card-rating">★ 4.4</span></div></div></div>
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
    document.querySelectorAll('#starPicker span').forEach((s, i) => s.classList.toggle('active', i < n));
  }
  function submitReview() {
    const text = document.getElementById('reviewText').value.trim();
    if (!selectedStars) { alert('Please select a star rating!'); return; }
    if (!text) { alert('Please write something before submitting!'); return; }
    const starStr = '⭐'.repeat(selectedStars);
    const today = new Date().toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' });
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `<div class="review-card-top"><div><div class="reviewer-name">You</div><div class="review-stars">${starStr}</div></div><div class="review-date">${today}</div></div><div class="review-text">${text}</div>`;
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
                <label class="hamburger" for="menu-toggle"><span></span><span></span><span></span></label>
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
                <h2 class="profile-name">{{ session.get('name', 'Name') }}</h2>
                <p class="profile-bio">{{ session.get('role', '').capitalize() }}</p>
                <button class="btn-edit">Edit Profile</button>
                <button class="btn-logout" onclick="window.location='{{ url_for('logout') }}'">Logout</button>
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


@app.route("/feedback")
def feedback():
    logged_in = session.get("logged_in", False)
    return render_template_string(HTML_FEEDBACK, logged_in=logged_in)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # DYNAMIC: add real authentication here later
        session["logged_in"] = True
        return redirect(url_for("index"))
    return render_template_string(HTML_LOGIN)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name")
        email    = request.form.get("email")
        password = request.form.get("password")
        role     = request.form.get("role")
        # DYNAMIC: save to DB here later
        session["logged_in"] = True
        session["role"]      = role
        session["name"]      = name
        session["email"]     = email
        return redirect(url_for("index"))
    return redirect(url_for("login") + "#signup")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ─────────────────────────────────────────────────────────────────
# FORGOT PASSWORD — Step 1: Enter Email
# ─────────────────────────────────────────────────────────────────
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error   = None
    prefill = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()

        # DYNAMIC: check if email exists in DB here later
        # For now we accept any non-empty email and generate a dummy code
        if not email:
            error = "Please enter your email address."
        else:
            code = str(random.randint(100000, 999999))
            session["reset_email"] = email
            session["reset_code"]  = code
            # DYNAMIC: send real email with code here later (e.g. via Flask-Mail)
            return redirect(url_for("verify_code"))

    return render_template_string(HTML_FORGOT, error=error, prefill=prefill)


# ─────────────────────────────────────────────────────────────────
# RESEND CODE — regenerates and redirects back to verify page
# ─────────────────────────────────────────────────────────────────
@app.route("/forgot-password/resend")
def forgot_password_resend():
    if "reset_email" not in session:
        return redirect(url_for("forgot_password"))
    code = str(random.randint(100000, 999999))
    session["reset_code"] = code
    # DYNAMIC: resend real email here later
    return redirect(url_for("verify_code"))


# ─────────────────────────────────────────────────────────────────
# VERIFY CODE — Step 2: Enter 6-digit code
# ─────────────────────────────────────────────────────────────────
@app.route("/verify-code", methods=["GET", "POST"])
def verify_code():
    if "reset_email" not in session:
        return redirect(url_for("forgot_password"))

    error    = None
    email    = session.get("reset_email", "")
    dev_code = session.get("reset_code", "------")   # shown in dev hint; remove in production

    if request.method == "POST":
        entered = request.form.get("code", "").strip()
        if entered == session.get("reset_code"):
            session["reset_verified"] = True
            return redirect(url_for("reset_password"))
        else:
            error = "Incorrect code. Please try again or request a new one."

    return render_template_string(HTML_VERIFY, email=email, dev_code=dev_code, error=error)


# ─────────────────────────────────────────────────────────────────
# RESET PASSWORD — Step 3: Set new password
# ─────────────────────────────────────────────────────────────────
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if not session.get("reset_verified"):
        return redirect(url_for("forgot_password"))

    error = None

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")
        if password != confirm:
            error = "Passwords do not match. Please try again."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            # DYNAMIC: update password in DB here later
            # Clear reset session keys after success
            session.pop("reset_email",    None)
            session.pop("reset_code",     None)
            session.pop("reset_verified", None)
            # The success screen is handled client-side in the template
            # so this POST redirect is a fallback
            return redirect(url_for("login"))

    return render_template_string(HTML_RESET, error=error)


if __name__ == "__main__":
    app.run(debug=True)