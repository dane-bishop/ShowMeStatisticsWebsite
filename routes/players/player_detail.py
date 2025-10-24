from .. import routes_bp
from flask import render_template, abort, request, url_for
from psycopg2.extras import RealDictCursor
import psycopg2
from core.get_db_connection import get_db_connection



@routes_bp.route("/players/<player_slug>")
def player_detail(player_slug: str):

    PLAYER_SQL = """
    SELECT
    p.id,
    p.full_name,
    p.player_slug,
    p.player_id       AS external_player_id,
    rm.position,
    rm.jersey,
    rm.class_year,
    rm.bats_throws,
    rm.hometown,
    rm.high_school,
    ts.year           AS season_year,
    t.school_name,
    s.name            AS sport_name
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts       ON rm.team_season_id = ts.id
    JOIN teams t               ON ts.team_id = t.id
    JOIN sports s              ON t.sport_id = s.id
    WHERE p.player_slug = %s
    ORDER BY ts.year DESC
    LIMIT 1;
    """

    SEASON_HIGHS_SQL = """
    SELECT
    stat_name,
    value,
    opponent_text,
    source_game_id,
    game_datetime
    FROM player_season_highs
    WHERE player_id = %s
    ORDER BY stat_name ASC;
    """


    GAMELOG_SQL = """
    SELECT
    pgb.id,
    pgb.source_game_id,
    pgb.wl,
    pgb.gs,
    pgb.ab, pgb.r, pgb.h, pgb.rbi,
    pgb.doubles, pgb.triples, pgb.hr,
    pgb.bb, pgb.ibb,
    pgb.sb, pgb.sba, pgb.cs,
    pgb.hbp, pgb.sh, pgb.sf, pgb.gdp, pgb.k,
    pgb.avg,
    g.game_date,        
    o.name AS opponent_name 
    FROM player_game_batting pgb
    LEFT JOIN games g ON g.id = pgb.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgb.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgb.id ASC;
    """




    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            
            # Player header
            cur.execute(PLAYER_SQL, (player_slug,))
            player = cur.fetchone()
            if not player:
                abort(404)

            # Season highs
            cur.execute(SEASON_HIGHS_SQL, (player["id"],))
            highs = cur.fetchall()

            # Game log
            cur.execute(GAMELOG_SQL, (player["id"],))
            gamelog = cur.fetchall()


            # Context-aware back URL
            from_team = request.args.get("from_team")
            from_year = request.args.get("year", type=int)

            if from_team and from_year:
                back_url = url_for("routes.team_roster", team_slug=from_team, team_year=from_year)

            else:
                ref = request.referrer or ""
                if "/teams/" in ref:
                    back_url = ref
                else:
                    back_url = url_for("routes.players")
        
        return render_template("player_detail.html", player=player, highs=highs, gamelog=gamelog, back_url=back_url)
    
    finally:
        conn.close()

    