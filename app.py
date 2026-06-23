from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, session
from reccsystem import recc_bp
from ratings import ratings_bp
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from flask import abort
from functools import wraps
import random
import os

app = Flask(__name__)

# ─── CONFIG ───
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SECRET_KEY'] = 'mmu-project-secret'

# ─── IMAGE UPLOAD CONFIG ───
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── EXTENSIONS ───
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'cynthia070607@gmail.com'  
app.config['MAIL_PASSWORD'] = 'mwet qoaa lqnu ckyv'             
app.config['MAIL_DEFAULT_SENDER'] = 'cynthia070607@gmail.com'

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ─── BLUEPRINTS ───
app.register_blueprint(recc_bp)
app.register_blueprint(ratings_bp)

reset_codes = {}

# ─── MODELS ───
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    avatar_file = db.Column(db.String(100), nullable=False, default='default_avatar.png')

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    stalls = db.relationship('Stall', backref='place', lazy=True)

class Stall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_type = db.Column(db.String(50))
    price_range = db.Column(db.String(10), nullable=False, default="RM")
    image_file = db.Column(db.String(100), nullable=False, default='default_stall.jpg')
    reviews = db.relationship('Review', backref='stall', cascade="all, delete-orphan", lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stall_id = db.Column(db.Integer, db.ForeignKey('stall.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('my_reviews', lazy=True))

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stall_id = db.Column(db.Integer, db.ForeignKey('stall.id'), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Optional: stores who sent it

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in allowed_roles:
                flash("Access denied. You do not have permission to view this page.")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ─── ROUTES ───
@app.route('/')
@app.route('/home')
def home():
    raw_categories = db.session.query(Stall.category.distinct()).all()
    categories_list = [c[0] for c in raw_categories if c[0]]

    query = request.args.get('q', '')
    selected_category = request.args.get('category')
    selected_price = request.args.get('price_range')
    selected_rating = request.args.get('rating')

    stall_query = Stall.query

    if query:
        stall_query = stall_query.join(Location).filter(Stall.name.ilike(f'%{query}%'))
    if selected_category:
        stall_query = stall_query.filter(Stall.category == selected_category)
    if selected_price:
        stall_query = stall_query.filter(Stall.price_range == selected_price)
    if selected_rating:
        pass
    stalls = stall_query.all()

    user_fav_ids = [] 
    if current_user.is_authenticated:
        favs = Favourite.query.filter_by(user_id=current_user.id).all()
        user_fav_ids = [f.stall_id for f in favs]

    return render_template(
                'homepage1.html', 
                stalls=stalls, 
                user_fav_ids=user_fav_ids,
                categories=categories_list,
                selected_category=selected_category,
                selected_price=selected_price,
                selected_rating=selected_rating,
                search_query=query
    )

@app.route('/toggle_favorite/<int:stall_id>', methods=['POST'])
def toggle_favorite(stall_id):
    if not current_user.is_authenticated:
        return jsonify({'status': 'unauthorized'}), 401
    
    stall = Stall.query.get_or_404(stall_id)
    existing_fav = Favourite.query.filter_by(user_id=current_user.id, stall_id=stall.id).first()

    if existing_fav:
        db.session.delete(existing_fav)
        action = 'removed'
    else:
        new_fav = Favourite(user_id=current_user.id, stall_id=stall.id)
        db.session.add(new_fav)
        action = 'added'

    db.session.commit()
    return jsonify({'status': 'success', 'action': action})
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        secret_code = request.form.get('secret_code', '').strip()

        if secret_code:
            if secret_code == "mMu2o26bruh":
                role = 'manager'
            else:
                flash("Invalid manager secret code. Please try again.")
                return redirect(url_for('register'))
        else:
            role = 'user'

        if not user_email or not user_password:
            flash("Email and Password fields are required.")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=user_email).first()
        if existing_user:
            flash("This email is already registered. Please log in.")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(user_password)
        new_user = User(name=user_name, email=user_email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('logreg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.email}!")
            if user.role == 'manager':
                return redirect(url_for('manager_dashboard'))
            return redirect(url_for('home'))
        else:
            flash("Login failed. Check your email and password.")
            return redirect(url_for('login'))

    return render_template('logreg.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/manager_dashboard')
@login_required
@role_required(['manager'])
def manager_dashboard():
    if current_user.role != 'manager':
        flash("Access denied. Managers only.")
        return redirect(url_for('home'))
    my_stalls = Stall.query.filter_by(manager_id=current_user.id).all()
    return render_template('manager_dashboard.html', stalls=my_stalls)

@app.route('/stall/<int:stall_id>')
def stall_details(stall_id):
    stall = Stall.query.get_or_404(stall_id)
    return render_template('stall.html', stall=stall)

@app.route('/stall/<int:stall_id>/review', methods=['POST'])
@login_required
def add_review(stall_id):
    stall = Stall.query.get_or_404(stall_id)
    existing_review = Review.query.filter_by(user_id=current_user.id, stall_id=stall.id).first()
    if existing_review:
        flash("You have already reviewed this stall! You can edit or delete your existing review below.")
        return redirect(url_for('stall_details', stall_id=stall.id))
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    if not rating or not comment:
        flash("Please provide a rating and a comment.")
        return redirect(url_for('stall_details', stall_id=stall.id))

    try:
        new_review = Review(
            rating=int(rating),
            comment=comment,
            user_id=current_user.id,
            stall_id=stall.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash("Review submitted successfully!")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while saving your review.")

    return redirect(url_for('stall_details', stall_id=stall.id))

@app.route('/review/edit/<int:review_id>', methods=['POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash("Unauthorized action.")
        return redirect(url_for('stall_details', stall_id=review.stall_id))

    new_rating = request.form.get('rating')
    new_comment = request.form.get('comment')

    if new_rating and new_comment:
        review.rating = int(new_rating)
        review.comment = new_comment
        db.session.commit()
        flash("Review updated successfully!")
    else:
        flash("All fields are required to update your review.")

    return redirect(url_for('stall_details', stall_id=review.stall_id))

@app.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    stall_id = review.stall_id

    if review.user_id == current_user.id or current_user.role == 'manager':
        db.session.delete(review)
        db.session.commit()
        flash("Review has been deleted.")
    else:
        flash("You do not have permission to delete this review.")

    return redirect(url_for('stall_details', stall_id=stall_id))


@app.route('/add_stall', methods=['GET', 'POST'])
@login_required
@role_required(['manager'])
def add_stall():
    if current_user.role != 'manager':
        flash("Access denied. Managers only.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        ftype = request.form.get('food_type')
        image_filename = 'default_stall.jpg'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_filename = filename
        price = request.form.get('price_range')
        new_stall = Stall(
            name=request.form.get('name'),
            location_id=int(request.form.get('location_id')),
            category=request.form.get('category'),
            description=request.form.get('description'),
            food_type=ftype,
            price_range=price,
            image_file=image_filename,
            manager_id=current_user.id
        )
        db.session.add(new_stall)
        db.session.commit()
        flash("Stall added successfully!")
        return redirect(url_for('manager_dashboard'))

    locations = Location.query.all()
    return render_template('add_stall.html', locations=locations)

@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    new_name = request.form.get('name')
    if new_name:
        current_user.name = new_name.strip()

    if 'avatar_image' in request.files:
        file = request.files['avatar_image']
        if file and file.filename != '':
            filename = secure_filename(f"user_{current_user.id}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.avatar_file = filename

    try:
        db.session.commit()
        flash("Profile updated successfully!")
    except Exception:
        db.session.rollback()
        flash("An error occurred while updating your profile.")

    return redirect(url_for('profile'))

@app.route('/edit_stall/<int:stall_id>', methods=['GET', 'POST'])
@login_required
@role_required(['manager'])
def edit_stall(stall_id):
    stall = Stall.query.get_or_404(stall_id)
    if stall.manager_id != current_user.id and current_user.role.lower() != 'admin':
        return "Unauthorized", 403
    if request.method == 'POST':
        stall.name = request.form.get('name')
        stall.category = request.form.get('category')
        stall.description = request.form.get('description')
        stall.location_id = int(request.form.get('location_id'))
        stall.food_type = request.form.get('food_type')
        stall.price_range = request.form.get('price_range')

        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                stall.image_file = filename

        db.session.commit()
        flash("Stall updated successfully!")
        return redirect(url_for('manager_dashboard'))

    locations = Location.query.all()
    return render_template('edit_stall.html', stall=stall, locations=locations)


@app.route('/delete_stall/<int:stall_id>', methods=['POST'])
@login_required
def delete_stall(stall_id):
    if current_user.role != 'manager':
        flash("Unauthorized access.")
        return redirect(url_for('home'))

    stall = Stall.query.get_or_404(stall_id)
    if stall.manager_id != current_user.id:
        flash("You do not have permission to delete this stall.")
        return redirect(url_for('home'))

    try:
        db.session.delete(stall)
        db.session.commit()
        flash(f"'{stall.name}' has been deleted successfully.")
        return redirect(url_for('manager_dashboard')) # ✅ FIXED: Smoothly redirects back to dashboard on success!
    except Exception:
        db.session.rollback()
        flash("Error occurred while deleting the stall.")
        return redirect(url_for('manager_dashboard'))


@app.route('/explore')
def explore():
    cat_filter = request.args.get('category')
    loc_filter = request.args.get('location')
    ftype = request.args.get('food_type')
    price = request.args.get('price_range')
    search = request.args.get('search')

    query = Stall.query

    if cat_filter:
        query = query.filter(Stall.category == cat_filter)
    if loc_filter:
        query = query.filter(Stall.location_id == loc_filter)
    if ftype:
        query = query.filter(Stall.food_type == ftype)
    if price:
        query = query.filter(Stall.price_range == price)
    if search:
        query = query.filter(Stall.name.contains(search))

    stalls = query.all()
    locations = Location.query.all()

    categories = db.session.query(Stall.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template('explore.html', stalls=stalls, locations=locations, categories=categories)


@app.route('/profile')
@login_required
def profile():
    favourites = Favourite.query.filter_by(user_id=current_user.id).all()

    fav_stalls = []
    for f in favourites:
        stall = Stall.query.get(f.stall_id)
        if stall: 
            fav_stalls.append(stall)

    reviews = Review.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', fav_stalls=fav_stalls, reviews=reviews)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        action = request.form.get('action')

        if action == 'send_code':
            user = User.query.filter_by(email=email).first()
            if user:
                code = str(random.randint(100000, 999999))
                expiration_time = datetime.now() + timedelta(minutes=5)
                
                # Save as a tuple
                reset_codes[email] = (code, expiration_time)
                
                print(f"DEBUG: Sent code {code} to {email}. Expires at {expiration_time}")
                flash("A reset code has been sent to your email.", "reset")
                return render_template('forgot_password.html', email=email, code_sent=True)
            
            flash("Email not found.")
            return render_template('forgot_password.html')

        elif action == 'verify_code':
            user_code = request.form.get('code')
            new_pw = request.form.get('new_password')
            
            if email in reset_codes:
                saved_code, expires_at = reset_codes[email]
                
                if datetime.now() > expires_at:
                    del reset_codes[email]
                    flash("Verification code has expired. Please request a new one.", "reset")
                    return redirect(url_for('forgot_password'))
                
                if saved_code == user_code:
                    user = User.query.filter_by(email=email).first()
                    user.password = generate_password_hash(new_pw)
                    db.session.commit()
                    
                    del reset_codes[email] 
                    flash("Password updated successfully.")
                    return redirect(url_for('login'))
            
            flash("Invalid or expired code.", "reset")
            return render_template('forgot_password.html', email=email, code_sent=True)
            
    return render_template('forgot_password.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Grab all the answers (including the useless fun ones!)
        fandom = request.form.get('fandom')   # Filler Q1
        mood = request.form.get('mood')       # Real filter Q2
        weather = request.form.get('weather') # Filler Q3
        budget = request.form.get('budget')   # Real filter Q4
        study = request.form.get('study')     # Filler Q5
        animal = request.form.get('animal')   # Filler Q6

        # Start with a base database query
        query = Stall.query

        # 🧠 MOOD MATRIX (From Q2): Translate human vibes directly into database partial matches
        vibe_title = "Foodie"
        if mood == 'chill':
            vibe_title = "The Calm & Collected Cafe-Hopper ☕"
            query = query.filter(
                (Stall.category.ilike('%cafe%')) |
                (Stall.category.ilike('%coffee%')) |
                (Stall.description.ilike('%chill%'))
            )
        elif mood == 'stressed':
            vibe_title = "The Overwhelmed Crammer (Needs a Hug) 🛋️"
            query = query.filter(
                (Stall.category.ilike('%malay%')) |
                (Stall.category.ilike('%nasi lemak%')) |
                (Stall.category.ilike('%comfort%'))
            )
        elif mood == 'social':
            vibe_title = "The Campus Squad Leader 🍕"
            query = query.filter(
                (Stall.category.ilike('%western%')) |
                (Stall.category.ilike('%pizza%')) |
                (Stall.category.ilike('%burger%'))
            )
        elif mood == 'hurry':
            vibe_title = "The Academic Speedrunner 🏃‍♂️"
            query = query.filter(
                (Stall.category.ilike('%fast%')) |
                (Stall.category.ilike('%snack%')) |
                (Stall.category.ilike('%indian%'))
            )

            # 💰 BUDGET MATRICES (From Q4): Filter by your uniform price strings
        if budget == 'low':
            query = query.filter(Stall.price_range == 'Under RM10')
        elif budget == 'medium':
            query = query.filter(Stall.price_range == 'RM10 - RM20')
        elif budget == 'high':
            query = query.filter(Stall.price_range == 'Above RM20')

        recommended_stalls = query.all()

                # 🔄 FALLBACK ENGINE: If the combined filters are too strict, give them general results for their mood
        if not recommended_stalls:
            if mood == 'chill':
                recommended_stalls = Stall.query.filter(Stall.category.ilike('%cafe%')).limit(3).all()
            elif mood == 'stressed':
                recommended_stalls = Stall.query.filter(Stall.category.ilike('%malay%')).limit(3).all()
            else:
                recommended_stalls = Stall.query.limit(3).all()

                        # Customizing the title ending using the useless Question 6 animal choice just for fun!
        animal_suffixes = {
            'cat': "🐾 (Cat Mode)",
        '    capybara': "🧘 (Capybara Energy)",
            'raccoon': "🦝 (Chaos Raccoon)"
                        }
        suffix = animal_suffixes.get(animal, "")
        final_vibe_name = f"{vibe_title} {suffix}"

        return render_template('suggest.html', stalls=recommended_stalls, vibe_name=final_vibe_name)

    return render_template('suggest.html')

# ─── DB INIT & RUN WITH ALTER-PATCH ───
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user_msg = request.form.get('comment')
        
        if not user_msg or user_msg.strip() == "":
            flash("Feedback text cannot be empty!")
            return redirect(url_for('feedback'))
            
        # Save only the text message to the independent Feedback table
        new_fb = Feedback(
            content=user_msg,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(new_fb)
        db.session.commit()
        
        flash("Thank you! Your feedback has been recorded.")
        return redirect(url_for('explore'))
        
    return render_template('feedback.html')

@app.route('/manager_feedback', methods=['GET', 'POST'])
@login_required
@role_required(['manager'])
def view_feedback():
    if current_user.role != 'manager':
        flash("Access denied. Managers only.")
        return redirect(url_for('explore'))
        
    all_feedbacks = Feedback.query.all()
    
    return render_template('manager_feedback.html', feedbacks=all_feedbacks)

with app.app_context():
    db.create_all()
    if not Location.query.first():
        buildings = ["Starbees MMU (Main)", "FCI Building", "FOE Building", "Library area"]
        for b in buildings:
            db.session.add(Location(name=b))
        db.session.commit()
        print("Database Initialized with Buildings.")
        
if __name__ == '__main__':
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    with app.app_context():
        db.create_all()

       
        try:
            db.session.execute(db.text("ALTER TABLE stall ADD COLUMN image_file VARCHAR(100) DEFAULT 'default_stall.jpg' NOT NULL;"))
            db.session.commit()
            print("Successfully applied patch: Added image_file column to Stall table.")
        except Exception:
            db.session.rollback()

           
        if not Location.query.first():
            buildings = ["Starbees MMU (Main)", "FCI Building", "FOE Building", "Library area"]
            for b in buildings:
                db.session.add(Location(name=b))
            db.session.commit()
            print("Database initialized with buildings.")


        #if not Stall.query.first():
           # loc = Location.query.first()
           # sample_stalls = [
           #     Stall(name="JINJJA SHYOK", category="western", location_id=loc.id),
            #    Stall(name="CITA RASA", category="malay", location_id=loc.id),
            #    Stall(name="Rasa Shiokk", category="malay", location_id=loc.id),
            #    Stall(name="Stall 4", category="chinese", location_id=loc.id),
           # ]
          #  db.session.add_all(sample_stalls)
          #  db.session.commit()
          #  print("Sample stalls added.")

app.run(debug=True)