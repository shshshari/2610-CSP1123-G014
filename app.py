from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mmu-project-secret'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    return "<h1>Welcome to MMU Food Finder!</h1><a href='/register'>Register Here</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        
        existing_user =User.query.filter_by(email=user_email).first()
        if existing_user:
            return "This email is already registered. Please use a different email."
        
        hashed_pw = generate_password_hash(user_password, method='sha256')
        new_user = User(email=user_email, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Login attempt received."
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #creates the physical database.db file
    app.run(debug=True)















