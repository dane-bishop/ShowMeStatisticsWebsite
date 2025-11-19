from flask import Flask, render_template, request
from flask_login import current_user
from .. import routes_bp
from routes.favorites.queries import fetch_favorite_players
from core.get_db_connection import get_db_connection
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor
from routes.home.queries.events import EVENTS_SQL

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

        # Get today's date
        today_ct = datetime.now(ZoneInfo("America/Chicago")).date()
        start_date = today_ct
        end_date = today_ct + timedelta(days=4)
        past_events_date = today_ct - timedelta(days=4)


        selected_sports = request.args.getlist("sports")

        base_sql = EVENTS_SQL
        

        upcoming_params = [start_date, end_date]

        past_params = [past_events_date, start_date]

        

        if selected_sports:
            base_sql += " And s.name = ANY(%s)"
            upcoming_params.append(selected_sports)

        
        base_sql += " ORDER BY g.game_date ASC, g.id ASC LIMIT 500;"
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Get upcoming events
            cur.execute(base_sql, upcoming_params)
            upcoming_events = cur.fetchall()


            # Get past events
            cur.execute(base_sql, past_params)
            past_events = cur.fetchall()



        

            fav_players = []
            if current_user.is_authenticated:
                fav_players = fetch_favorite_players(conn, current_user.id, limit=24)
            


        return render_template(
            "index.html",
            men_sports=MEN_SPORTS,
            women_sports=WOMEN_SPORTS,
            upcoming_events=upcoming_events,
            past_events=past_events,
            headlines=HEADLINE_ITEMS,
            selected_sports=selected_sports,
            fav_players=fav_players,
            start_date=start_date,
            end_date=end_date,
        )
    

    finally:
        conn.close()
