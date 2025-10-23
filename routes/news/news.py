from .. import routes_bp
from flask import render_template


HEADLINE_ITEMS = [
    {"headline": "Tigers upset #5 Wildcats in overtime thriller", "date": "2025-10-06"},
    {"headline": "Season preview: Men's Basketball poised for breakout", "date": "2025-10-05"},
]

@routes_bp.route("/news")
def news():
    return render_template("news.html", headlines=HEADLINE_ITEMS)