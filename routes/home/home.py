from flask import Flask, render_template, request
from flask_login import current_user
from .. import routes_bp
from routes.favorites.queries import fetch_favorite_players
from core.get_db_connection import get_db_connection
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, date
from psycopg2.extras import RealDictCursor
from routes.home.queries.events import EVENTS_SQL
import calendar
from core.helpers.shift_month import shift_month
from routes.home.queries.game_calendar import GAME_CALENDAR_SQL

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
        past_events_start_date = today_ct - timedelta(days=1)


        selected_sports = request.args.getlist("sports")
        base_sql = EVENTS_SQL
        upcoming_params = [start_date, end_date]
        past_params = [past_events_date, past_events_start_date]


        # CALENDAR PARAMETERS
        month_param = request.args.get("month")  # e.g. '2025-11'
        today = date.today

        if month_param:
            try:
                cal_year, cal_month = map(int, month_param.split("-"))
            except ValueError:
                cal_year, cal_month = today_ct.year, today_ct.month
        else:
            cal_year, cal_month = today_ct.year, today_ct.month

        

        first_day = date(cal_year, cal_month, 1)
        _, last_day_num = calendar.monthrange(cal_year, cal_month)
        last_day = date(cal_year, cal_month, last_day_num)

        prev_year, prev_month = shift_month(cal_year, cal_month, -1)
        next_year, next_month = shift_month(cal_year, cal_month, +1)

        prev_month_str = f"{prev_year}-{prev_month:02d}"
        next_month_str = f"{next_year}-{next_month:02d}"
        current_month_str = f"{cal_year}-{cal_month:02d}"
        calendar_label = first_day.strftime("%B %Y")
            


        calendar_sql = GAME_CALENDAR_SQL
        calendar_params = [first_day, last_day]


        if selected_sports:
            base_sql += " And s.name = ANY(%s)"
            upcoming_params.append(selected_sports)
            past_params.append(selected_sports)
            calendar_sql = GAME_CALENDAR_SQL.replace(
                    "WHERE g.game_date BETWEEN %s AND %s",
                    "WHERE g.game_date BETWEEN %s AND %s AND s.name = ANY(%s)"
                )
            calendar_params.append(selected_sports)

        
        base_sql += " ORDER BY g.game_date ASC, g.id ASC LIMIT 500;"


        

        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Get upcoming events
            cur.execute(base_sql, upcoming_params)
            upcoming_events = cur.fetchall()


            # Get past events
            cur.execute(base_sql, past_params)
            past_events = cur.fetchall()


            

            cur.execute(calendar_sql, calendar_params)
            calendar_rows = cur.fetchall()



        

            fav_players = []
            if current_user.is_authenticated:
                fav_players = fetch_favorite_players(conn, current_user.id, limit=24)
            


        # Group games by date string "YYYY-MM-DD"
        games_by_date: dict[str, list[dict]] = {}
        for row in calendar_rows:
            key = row["game_date"].isoformat()
            games_by_date.setdefault(key, []).append(row)

        # Build a matrix of week rows (each week = 7 date objects)
        cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday
        calendar_weeks = list(cal.monthdatescalendar(cal_year, cal_month))




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


            calendar_weeks=calendar_weeks,
            games_by_date=games_by_date,
            calendar_label=calendar_label,
            calendar_prev=prev_month_str,
            calendar_next=next_month_str,
            calendar_current=current_month_str,
            calendar_year=cal_year,
            calendar_month=cal_month,
        )
    

    finally:
        conn.close()
