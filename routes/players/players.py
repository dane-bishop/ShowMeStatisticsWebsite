from flask import render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import routes_bp
from core.get_db_connection import get_db_connection


@routes_bp.route("/players")
def players():


    

    
    sql = """
    SELECT DISTINCT
    p.id, p.full_name, s.name AS team_name, rm.position, p.player_slug
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts ON rm.team_season_id = ts.id
    JOIN teams t ON ts.team_id = t.id
    JOIN sports s ON t.sport_id = s.id
    ORDER BY name;
    """

    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        players = cur.fetchall()
    
    return render_template("players.html", players=players)