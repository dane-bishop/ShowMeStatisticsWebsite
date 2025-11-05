from .. import routes_bp
from flask import render_template, abort, request, url_for
from psycopg2.extras import RealDictCursor
import psycopg2
from core.get_db_connection import get_db_connection
from flask_login import current_user



@routes_bp.route("/players/<player_slug>")
def player_detail_baseball(player_slug: str):

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


    GAMELOG_HITTING_SQL = """
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

    GAMELOG_PITCHING_SQL = """
    SELECT
    pgp.id,
    pgp.source_game_id,
    pgp.wl,
    pgp.ip, pgp.h, pgp.r, pgp.er, pgp.bb, pgp.so, pgp.doubles, pgp.triples,
    pgp.hr, pgp.wp, pgp.bk, pgp.hbp, pgp.ibb, pgp.np, pgp.w, pgp.l, pgp.sv, pgp.gera, pgp.sera,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_pitching pgp
    JOIN games g ON g.id = pgp.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgp.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgp.id ASC;
    """

    GAMELOG_FIELDING_SQL = """
    SELECT
    pgf.id, pgf.source_game_id, pgf.wl,
    pgf.c, pgf.po, pgf.a, pgf.e, pgf.fld, pgf.dp, pgf.sba, pgf.csb, pgf.pb, pgf.ci,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_fielding pgf
    JOIN games g ON g.id = pgf.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgf.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgf.id ASC;
    """

    IS_FAVORITE_SQL = """
    SELECT 1 
    FROM favorites
    WHERE user_id = %s AND entity_type = 'player' AND entity_id = %s
    LIMIT 1
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

            # Game log hitting
            cur.execute(GAMELOG_HITTING_SQL, (player["id"],))
            gamelog_hitting = cur.fetchall()

            # Game log pitching
            cur.execute(GAMELOG_PITCHING_SQL, (player["id"],))
            gamelog_pitching = cur.fetchall()

            # Game log fielding
            cur.execute(GAMELOG_FIELDING_SQL, (player["id"],))
            gamelog_fielding = cur.fetchall()

            # Is player favorite
            is_favorited = False
            if current_user.is_authenticated:
                cur.execute(IS_FAVORITE_SQL, (int(current_user.id), player["id"]))
                is_favorited = cur.fetchone() is not None



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
        
        return render_template("player_detail_baseball.html", player=player, highs=highs, gamelog_hitting=gamelog_hitting, gamelog_pitching=gamelog_pitching, gamelog_fielding=gamelog_fielding, is_favorited=is_favorited, back_url=back_url)
    
    finally:
        conn.close()

    