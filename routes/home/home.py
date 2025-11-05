from flask import Flask, render_template, request
from flask_login import current_user
from .. import routes_bp
from routes.favorites.queries import fetch_favorite_players
from core.get_db_connection import get_db_connection

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




@routes_bp.route("/")
def home():
    conn = get_db_connection()
    try:
        
        selected_sports = request.args.getlist("sports")
        if selected_sports:
            filtered = [e for e in SAMPLE_EVENTS if e["sport"] in selected_sports]
        else:
            filtered = SAMPLE_EVENTS


        

        fav_players = []
        if current_user.is_authenticated:
            fav_players = fetch_favorite_players(conn, current_user.id, limit=24)
        


        return render_template(
        "index.html",
        men_sports=MEN_SPORTS,
        women_sports=WOMEN_SPORTS,
        events=filtered,
        headlines=HEADLINE_ITEMS,
        selected_sports=selected_sports,
        fav_players=fav_players)
    

    finally:
        conn.close()
