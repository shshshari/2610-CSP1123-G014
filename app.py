from flask import Flask
from recc_routes import recc_bp

app = Flask(__name__)
app.secret_key = "placeholder_secret_key" 


app.register_blueprint(recc_bp)

if __name__ == "__main__":
    app.run(debug=True)