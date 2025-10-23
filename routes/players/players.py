from flask import render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import routes_bp


@routes_bp.route("/players")
def players():


    def get_db_connection():
        return psycopg2.connect(host="localhost", database="capstone_db", user="danebishop",password="Bayloreagles20")

    
    sql = """
    SELECT DISTINCT
    p.id, p.full_name, s.name, rm.position
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