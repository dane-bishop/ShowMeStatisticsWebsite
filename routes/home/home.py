from flask import Flask, render_template, request
from flask_login import current_user
from .. import routes_bp
from routes.favorites.queries import fetch_favorite_players
from core.get_db_connection import get_db_connection
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor

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



HEADLINE_ITEMS = [
    {"headline": "Tigers upset #5 Wildcats in overtime thriller", "date": "2025-10-06"},
    {"headline": "Season preview: Men's Basketball poised for breakout", "date": "2025-10-05"},
]




@routes_bp.route("/")
def home():
    conn = get_db_connection()
    try:


        today_ct = datetime.now(ZoneInfo("America/Chicago")).date()
        start_date = today_ct
        end_date = today_ct + timedelta(days=4)

        selected_sports = request.args.getlist("sports")

        EVENTS_SQL = """
        SELECT
            g.id,
            g.game_date,
            s.name AS sport_name,
            t.school_name,
            o.name AS opponent_name,
            g.location,
            g.source_game_id
        FROM games g
        JOIN team_seasons ts ON ts.id = g.team_season_id
        JOIN teams t ON t.id = ts.team_id
        JOIN sports s ON s.id = t.sport_id
        LEFT JOIN opponents o ON o.id = g.opponent_id
        WHERE g.game_date >= %s AND g.game_date <= %s
        """

        params = [start_date, end_date]

        if selected_sports:
            EVENTS_SQL += " And s.name = ANY(%s)"
            params.append(selected_sports)

        EVENTS_SQL += " ORDER BY g.game_date ASC, g.id ASC LIMIT 500;"

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(EVENTS_SQL, params)
            events = cur.fetchall()
        

            fav_players = []
            if current_user.is_authenticated:
                fav_players = fetch_favorite_players(conn, current_user.id, limit=24)
            


        return render_template(
            "index.html",
            men_sports=MEN_SPORTS,
            women_sports=WOMEN_SPORTS,
            events=events,
            headlines=HEADLINE_ITEMS,
            selected_sports=selected_sports,
            fav_players=fav_players,
            start_date=start_date,
            end_date=end_date,
        )
    

    finally:
        conn.close()
