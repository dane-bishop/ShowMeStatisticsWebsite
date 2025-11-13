from flask import render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import routes_bp
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

@routes_bp.route("/players")
def players():
    # Get filter parameters from query string
    gender_filter = request.args.get("gender", "all")  # 'men', 'women', 'all'
    sport_filter = request.args.get("sport", "all")    # sport name or 'all'
    year_filter = request.args.get("year", "all")      # year or 'all'

    sql = """
    SELECT DISTINCT
    p.id, p.full_name, s.name AS sport_name, s.key AS team_slug, rm.position, p.player_slug, ts.year
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts ON rm.team_season_id = ts.id
    JOIN teams t ON ts.team_id = t.id
    JOIN sports s ON t.sport_id = s.id
    WHERE p.player_slug IS NOT NULL AND p.player_slug <> ''
    ORDER BY p.full_name, ts.year DESC;
    """

    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        all_players = cur.fetchall()
    
    # Filter players based on criteria
    filtered_players = all_players
    
    # Apply gender filter
    if gender_filter == "men":
        filtered_players = [p for p in filtered_players if p['sport_name'] in MEN_SPORTS]
    elif gender_filter == "women":
        filtered_players = [p for p in filtered_players if p['sport_name'] in WOMEN_SPORTS]
    
    # Apply sport filter
    if sport_filter != "all":
        filtered_players = [p for p in filtered_players if p['sport_name'] == sport_filter]
    
    # Apply year filter
    if year_filter != "all":
        try:
            year_int = int(year_filter)
            filtered_players = [p for p in filtered_players if p['year'] == year_int]
        except ValueError:
            pass
    
    # Get available years for filter dropdown
    available_years = sorted(set(p['year'] for p in all_players), reverse=True)
    
    # Get available sports for filter dropdown
    all_sports = sorted(set(p['sport_name'] for p in all_players))
    
    return render_template(
        "players.html", 
        players=filtered_players,
        all_players=all_players,
        available_years=available_years,
        all_sports=all_sports,
        gender_filter=gender_filter,
        sport_filter=sport_filter,
        year_filter=year_filter
    )