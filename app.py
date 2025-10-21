from flask import Flask, render_template, url_for, redirect, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# still like having seperate sections in the home page for mens and womens
# but have to have sports prefixed with either men or woman bc otherwise the dropdowns
# wont work properly bc itll read basketball as 1 and not mens and womens, atp you 
# have to uncheck or check both for them to work properly
MEN_SPORTS = [
    "Men's Basketball", "Men's Baseball", "Men's Cross Country", "Men's Football",
    "Men's Golf", "Men's Swim & Dive", "Men's Track & Field", "Men's Wrestling"
]

WOMEN_SPORTS = [
    "Women's Basketball", "Women's Cross Country", "Women's Golf",
    "Women's Gymnastics", "Women's Soccer", "Women's Softball",
    "Women's Swim & Dive", "Women's Tennis", "Women's Track & Field",
    "Women's Volleyball"
]

SAMPLE_EVENTS = [
    {
        "id": 1,
        "date": "2025-10-08",
        "sport": "Football",
        "title": "Tigers vs Wildcats",
        "location": "Memorial Stadium",
        "opponent_team": "Wildcats",
        "opponent_record": "4-1",
        "opponent_name": "Kansas State Wildcats",
    },
    {
        "id": 2,
        "date": "2025-10-10",
        "sport": "Basketball",
        "title": "Tigers vs Bears",
        "location": "Mizzou Arena",
        "opponent_team": "Bears",
        "opponent_record": "2-0",
        "opponent_name": "Missouri State Bears",
    },
    {
        "id": 3,
        "date": "2025-10-12",
        "sport": "Soccer",
        "title": "Tigers vs Lions",
        "location": "Walton Stadium",
        "opponent_team": "Lions",
        "opponent_record": "3-2-1",
        "opponent_name": "Lindenwood Lions",
    },
    {
        "id": 4,
        "date": "2025-10-15",
        "sport": "Baseball",
        "title": "Tigers vs Hawks",
        "location": "Taylor Stadium",
        "opponent_team": "Hawks",
        "opponent_record": "5-3",
        "opponent_name": "Saint Joseph Hawks",
    },
]

HEADLINE_ITEMS = [
    {"headline": "Tigers upset #5 Wildcats in overtime thriller", "date": "2025-10-06"},
    {"headline": "Season preview: Men's Basketball poised for breakout", "date": "2025-10-05"},
]

TEAMS = [
    {"name": s, "slug": s.lower().replace(" ", "-").replace("&", "and").replace("'", "")}
    for s in MEN_SPORTS + WOMEN_SPORTS
]

#home page
@app.route("/")
def home():
    selected_sports = request.args.getlist("sports")
    if selected_sports:
        filtered = [e for e in SAMPLE_EVENTS if e["sport"] in selected_sports]
    else:
        filtered = SAMPLE_EVENTS

    return render_template(
    "index.html",
    men_sports=MEN_SPORTS,
    women_sports=WOMEN_SPORTS,
    events=filtered,
    headlines=HEADLINE_ITEMS,
    selected_sports=selected_sports,
)

#teams page
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







#players page
@app.route("/players")
def players():



    sample_players = [
        {"name": "Alex Johnson", "team": "Football", "position": "QB"},
        {"name": "Sam Lee", "team": "Men's Basketball", "position": "G"},
        {"name": "Taylor Smith", "team": "Women's Soccer", "position": "FW"},
    ]

    sql = """
    SELECT DISTINCT
    p.id, p.full_name, s.name, rm.position
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts ON rm.team_season_id = ts.id
    JOIN teams t ON ts.team_id = t.id
    JOIN sports s ON t.sport_id = s.id
    ORDER BY name;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        players = cur.fetchall()

    return render_template("players.html", players=players)







#scores page
@app.route("/scores")
def scores():
    recent_scores = [
        {"sport": "Football", "opponent": "Wildcats", "result": "W 27-24", "date": "2025-10-06"},
        {"sport": "Women's Soccer", "opponent": "Lions", "result": "D 1-1", "date": "2025-10-05"},
        {"sport": "Baseball", "opponent": "Hawks", "result": "L 3-4", "date": "2025-10-02"},
    ]
    return render_template("scores.html", scores=recent_scores)

@app.route("/game/<int:game_id>")
def game_detail(game_id: int):
    game = next((g for g in SAMPLE_EVENTS if g["id"] == game_id), None)
    if not game:
        return redirect(url_for("home"))
    # Placeholder: derive home/away info etc. Here we show passed metadata
    return render_template("game_detail.html", game=game)

#profile page
@app.route("/profile")
def profile():
    # Placeholder: not authenticated logic yet
    return render_template("profile.html", has_account=False)

#search function
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    # Simple placeholder search across team names
    team_results = [t for t in TEAMS if q.lower() in t["name"].lower()] if q else []
    return render_template("search_results.html", query=q, team_results=team_results)

#news page
@app.route("/news")
def news():
    return render_template("news.html", headlines=HEADLINE_ITEMS)

if __name__ == "__main__":
    app.run(debug=True)
