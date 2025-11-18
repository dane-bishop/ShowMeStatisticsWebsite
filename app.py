from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager
from routes.auth.auth import load_user_by_id
from psycopg2.extras import RealDictCursor
import psycopg2
from routes import routes_bp
from routes.auth import auth_bp
from routes.favorites import favorites_bp
from routes import profile
import os


def create_app():
    app = Flask(__name__)

    secret = os.environ.get("SECRET_KEY")
    if not secret:
        # Optional: allow a dev fallback locally
        # secret = "dev-only-not-secure"
        raise RuntimeError("FLASK_SECRET_KEY is not set")
    
    app.config["SECRET_KEY"] = secret

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(favorites_bp)
    return app

app = create_app()


login_manager = LoginManager()
login_manager.login_view = "auth.login_form"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: str):
    return load_user_by_id(user_id)



if __name__ == "__main__":
    app.run(debug=True)
