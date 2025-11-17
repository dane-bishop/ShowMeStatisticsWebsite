from .. import routes_bp
from flask import request, render_template
from routes.home.queries.player_search import PLAYER_SEARCH_SQL
from routes.home.queries.team_search import TEAM_SEARCH_SQL
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor


@routes_bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    
    page = max(int(request.args.get("page", 1)), 1)
    limit = 25
    offset = (page - 1) * limit
    if not q:
        return render_template(
            "etc/search_results.html",
            query=q,
            player_results=[],
            team_results=[],
            page=page,
            more_players=False,
            more_teams=False,
        )
    
    pat = f"%{q}%"

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(PLAYER_SEARCH_SQL, {"pat": pat, "limit": limit, "offset": offset})
            player_results = cur.fetchall()

            cur.execute(TEAM_SEARCH_SQL, {"pat": pat, "limit": limit, "offset": offset})
            team_results = cur.fetchall()

        more_players = len(player_results) == limit
        more_teams = len(team_results) == limit

        return render_template(
            "etc/search_results.html",
            query=q,
            player_results=player_results,
            team_results=team_results,
            page=page,
            more_players=more_players,
            more_teams=more_teams,
        )


    finally:
        conn.close()

    

    
