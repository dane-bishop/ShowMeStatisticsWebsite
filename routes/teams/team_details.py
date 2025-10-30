from .. import routes_bp
from flask import redirect, url_for, render_template, request, abort
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor





@routes_bp.route("/teams/<team_slug>")
@routes_bp.route("/teams/<team_slug>/<int:team_year>")
def team_detail(team_slug: str, team_year: int | None = None):


    team_sql = """
    SELECT 
    t.site_slug AS slug,
    CONCAT(t.school_name, ' ', s.name) AS name
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    WHERE t.site_slug = %s
    LIMIT 1;
    """

    team_schedule_sql = """
    SELECT 
    o.name AS opponent_name,
    g.game_date,
    g.location,
    g.result,
    g.score_for,
    g.score_against,
    g.game_time,
    g.game_number
    FROM games g
    JOIN opponents o ON o.id = g.opponent_id
    JOIN team_seasons ts ON ts.id = g.team_season_id
    JOIN teams t ON t.id = ts.team_id
    WHERE t.site_slug = %s AND ts.year = %s
    ORDER BY g.game_date asc;

    """

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(team_sql, (team_slug,))
            team = cur.fetchone()
            if not team:
                abort(404)

            # default year if not provided: latest season for this team
            if team_year is None:
                cur.execute("""
                    SELECT MAX(ts.year) AS latest
                    FROM team_seasons ts
                    JOIN teams t ON t.id = ts.team_id
                    WHERE t.site_slug = %s
                """, (team_slug,))
                row = cur.fetchone()
                team_year = row["latest"]

            # schedule
            cur.execute(team_schedule_sql, (team_slug, team_year))
            team_schedule = cur.fetchall()

        


    finally:
        conn.close()

    news = [
        
    ]
    

    return render_template("team_detail.html", team=team, events=team_schedule, news=news, team_year=team_year)