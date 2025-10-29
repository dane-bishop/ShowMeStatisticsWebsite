from .. import routes_bp
from flask import request, render_template

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


TEAMS = [
    {"name": s, "slug": s.lower().replace(" ", "-").replace("&", "and").replace("'", "")}
    for s in MEN_SPORTS + WOMEN_SPORTS
]

@routes_bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    # Simple placeholder search across team names
    team_results = [t for t in TEAMS if q.lower() in t["name"].lower()] if q else []
    return render_template("search_results.html", query=q, team_results=team_results)


