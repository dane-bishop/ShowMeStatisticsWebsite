from flask import Flask, render_template, url_for, redirect, request

from psycopg2.extras import RealDictCursor
import psycopg2
from routes import routes_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)
    return app

app = create_app()



if __name__ == "__main__":
    app.run(debug=True)
