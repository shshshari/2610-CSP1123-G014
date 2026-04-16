from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mmu-project-secret'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')

@app.route('/')
def home():
    return "<h1>Welcome to MMU Food Finder!</h1><a href='/register'>Register Here</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        role = request.form.get('role')

        if role == 'manager':
            secret_code = request.form.get('secret_code')
            if secret_code != "mMu2o26bruh":
                flash("Invalid manager secret code. Please try again.")
                return redirect(url_for('register'))
        
        existing_user =User.query.filter_by(email=user_email).first()
        if existing_user:
            flash("This email is already registered. Please use a different email.")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(user_password)
        new_user = User(email=user_email, password=hashed_pw, role=role)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

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
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))

@app.route('/manager_dashboard')
@login_required
def manager_dashboard():
    if current_user.role != 'manager':
        flash("Access denied. Managers only.")
    return "<h1>Manager Dashboard</h1><p>welcome, manager!</p><a href='/logout'>Logout</a>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #creates the physical database.db file
    app.run(debug=True)















