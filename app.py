from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

SPORTS = [
    "Men's Basketball", "Baseball", "Men's Cross Country", "Football", "Men's Golf",
    "Men's Swim & Dive", "Men's Track & Field", "Wrestling", "Women's Basketball",
    "Women's Cross Country", "Women's Golf", "Gymnastics", "Women's Soccer",
    "Softball", "Women's Swim & Dive", "Women's Tennis", "Women's Track & Field",
    "Women's Volleyball"
]

SAMPLE_EVENTS = [
    {"date": "2025-10-08", "sport": "Football", "title": "Tigers vs Wildcats", "location": "Memorial Stadium"},
    {"date": "2025-10-10", "sport": "Men's Basketball", "title": "Tigers vs Bears", "location": "Mizzou Arena"},
    {"date": "2025-10-12", "sport": "Women's Soccer", "title": "Tigers vs Lions", "location": "Walton Stadium"},
    {"date": "2025-10-15", "sport": "Baseball", "title": "Tigers vs Hawks", "location": "Taylor Stadium"},
]

HEADLINE_ITEMS = [
    {"headline": "Tigers upset #5 Wildcats in overtime thriller", "date": "2025-10-06"},
    {"headline": "Season preview: Men's Basketball poised for breakout", "date": "2025-10-05"},
]

TEAMS = [
    {"name": s, "slug": s.lower().replace(" ", "-").replace("&", "and").replace("'", "")}
    for s in SPORTS
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        sports=SPORTS,
        events=SAMPLE_EVENTS,
        headlines=HEADLINE_ITEMS,
    )

@app.route("/teams")
def teams():
    return render_template("teams.html", teams=TEAMS)

@app.route("/teams/<team_slug>")
def team_detail(team_slug: str):
    team = next((t for t in TEAMS if t["slug"] == team_slug), None)
    if team is None:
        return redirect(url_for("teams"))

    team_events = [e for e in SAMPLE_EVENTS if team["name"] in e["sport"] or e["sport"] in team["name"]]
    news = [
        {"title": f"{team['name']} ready for conference play", "date": "2025-10-03"},
        {"title": f"Rookie stars in {team['name']} scrimmage", "date": "2025-10-01"},
    ]
    return render_template("team_detail.html", team=team, events=team_events, news=news)

@app.route("/players")
def players():
    sample_players = [
        {"name": "Alex Johnson", "team": "Football", "position": "QB"},
        {"name": "Sam Lee", "team": "Men's Basketball", "position": "G"},
        {"name": "Taylor Smith", "team": "Women's Soccer", "position": "FW"},
    ]
    return render_template("players.html", players=sample_players)

@app.route("/scores")
def scores():
    recent_scores = [
        {"sport": "Football", "opponent": "Wildcats", "result": "W 27-24", "date": "2025-10-06"},
        {"sport": "Women's Soccer", "opponent": "Lions", "result": "D 1-1", "date": "2025-10-05"},
        {"sport": "Baseball", "opponent": "Hawks", "result": "L 3-4", "date": "2025-10-02"},
    ]
    return render_template("scores.html", scores=recent_scores)

@app.route("/profile")
def profile():
    # Placeholder: not authenticated logic yet
    return render_template("profile.html", has_account=False)

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    # Simple placeholder search across team names
    team_results = [t for t in TEAMS if q.lower() in t["name"].lower()] if q else []
    return render_template("search_results.html", query=q, team_results=team_results)

if __name__ == "__main__":
    app.run(debug=True)
