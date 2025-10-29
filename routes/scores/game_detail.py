from .. import routes_bp
from flask import redirect, render_template, url_for


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

@routes_bp.route("/game/<int:game_id>")
def game_detail(game_id: int):
    game = next((g for g in SAMPLE_EVENTS if g["id"] == game_id), None)
    if not game:
        return redirect(url_for("home"))
    # Placeholder: derive home/away info etc. Here we show passed metadata
    return render_template("game_detail.html", game=game)