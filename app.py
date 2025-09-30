from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", page="Home")

@app.route("/teams")
def teams():
    return render_template("index.html", page="Teams")

@app.route("/players")
def players():
    return render_template("index.html", page="Players")

@app.route("/scores")
def scores():
    return render_template("index.html", page="Scores")

if __name__ == "__main__":
    app.run(debug=True)
