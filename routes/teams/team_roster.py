from .. import routes_bp
from flask import render_template, abort, url_for
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection
from flask_login import current_user
from routes.teams.queries.favorites import FAVORITES_SQL
from routes.teams.queries.team import TEAM_SQL
from routes.teams.queries.roster import ROSTER_SQL



@routes_bp.route("/teams/<team_slug>/<int:team_year>/roster")
def team_roster(team_slug: str, team_year: int):
    


    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(TEAM_SQL, (team_slug,))
            team = cur.fetchone()
            
            
            cur.execute(ROSTER_SQL, (team_slug, team_year))
            roster = cur.fetchall()

            """
            if current_user.is_authenticated:
                cur.execute(FAVORITES_SQL, (current_user.id,))
                fav_player_ids = {row[0] for row in cur.fetchall()} """

            news = [
                {"title": f"{team['school_name']} {team['sport_name']} roster for {team_year}", "date": str(team_year)},
            ]

            return render_template("team_roster.html", team=team, team_year=team_year, roster=roster, news=news)

    finally:
        conn.close()