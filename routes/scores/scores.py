from .. import routes_bp
from flask import render_template


@routes_bp.route("/scores")
def scores():
    recent_scores = [
        {"sport": "Football", "opponent": "Wildcats", "result": "W 27-24", "date": "2025-10-06"},
        {"sport": "Women's Soccer", "opponent": "Lions", "result": "D 1-1", "date": "2025-10-05"},
        {"sport": "Baseball", "opponent": "Hawks", "result": "L 3-4", "date": "2025-10-02"},
    ]
    return render_template("scores.html", scores=recent_scores)