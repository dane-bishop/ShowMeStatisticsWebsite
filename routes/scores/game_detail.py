from .. import routes_bp
from flask import redirect, render_template, url_for
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor
from routes.scores.game_detail_queries.game import GAME_SQL



PLAYER_HITTING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgb.ab, pgb.r, pgb.h, pgb.rbi,
    pgb.doubles, pgb.triples, pgb.hr,
    pgb.bb, pgb.ibb,
    pgb.sb, pgb.sba, pgb.cs,
    pgb.hbp, pgb.sh, pgb.sf, pgb.gdp, pgb.k,
    pgb.avg
    FROM player_game_batting pgb
    JOIN games g ON g.id = pgb.game_id
    JOIN players p ON p.id = pgb.player_id
    JOIN roster_memberships rm ON rm.player_id = p.id
    WHERE pgb.game_id = %s
    ORDER BY rm.jersey ASC;
    """

PLAYER_PITCHING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgp.ip, pgp.h, pgp.r, pgp.er, pgp.bb, pgp.so, pgp.doubles, pgp.triples,
    pgp.hr, pgp.wp, pgp.bk, pgp.hbp, pgp.ibb, pgp.np, pgp.w, pgp.l, pgp.sv, pgp.gera, pgp.sera
    FROM player_game_pitching pgp
    JOIN games g ON g.id = pgp.game_id
    JOIN players p ON p.id = pgp.player_id
    JOIN roster_memberships rm ON rm.player_id = p.id
    WHERE pgp.game_id = %s
    ORDER BY rm.jersey ASC;
    """

PLAYER_FIELDING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgf.c, pgf.po, pgf.a, pgf.e, pgf.fld, pgf.dp, pgf.sba, pgf.csb, pgf.pb, pgf.ci
    FROM player_game_fielding pgf
    JOIN games g ON g.id = pgf.game_id
    JOIN players p ON p.id = pgf.player_id
    JOIN roster_memberships rm ON rm.player_id = p.id
    WHERE pgf.game_id = %s
    ORDER BY rm.jersey ASC;
    """


PLAYER_FOOTBALL_OFFENSE_STATS_SQL = """
    SELECT 
    p.full_name,
    rm.jersey,
    pgfo.pass_comp, pgfo.pass_att, pgfo.pass_int, pgfo.pass_pct,
    pgfo.pass_yds, pgfo.pass_tds, pgfo.pass_lng,
    pgfo.rush_att, pgfo.rush_yds, pgfo.rush_tds, pgfo.rush_lng,
    pgfo.rec, pgfo.rec_yds, pgfo.rec_tds, pgfo.rec_lng,
    pgfo.kr_ret, pgfo.kr_yds, pgfo.kr_tds, pgfo.kr_lng,
    pgfo.pr_ret, pgfo.pr_yds, pgfo.pr_tds, pgfo.pr_lng
    FROM player_game_football_offense pgfo
    JOIN games g ON g.id = pgfo.game_id
    JOIN players p ON p.id = pgfo.player_id
    JOIN roster_memberships rm ON rm.player_id = p.id
    WHERE pgfo.game_id = %s
    ORDER BY rm.jersey ASC;
    """

PLAYER_FOOTBALL_DEFENSE_STATS_SQL = """
    SELECT 
    p.full_name,
    rm.jersey,
    pgfd.solo, pgfd.ast, pgfd.ttot, pgfd.tfl, pgfd.tyds,
    pgfd.stot, pgfd.syds,
    pgfd.ff, pgfd.fr, pgfd.fyds,
    pgfd.ints, pgfd.int_yds,
    pgfd.qbh, pgfd.brk, pgfd.kick, pgfd.saf
    FROM player_game_football_defense pgfd
    JOIN games g ON g.id = pgfd.game_id
    JOIN roster_memberships rm ON rm.player_id = p.id
    WHERE pgfd.game_id = %s
    ORDER BY rm.jersey ASC;
    """

@routes_bp.route("/game/<int:game_id>")
def game_detail(game_id: int):


    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(GAME_SQL, (game_id,))
            game = cur.fetchone()

            context = {
                "game": game,
            }

            sport_name = (game.get("sport_name"))

            if sport_name == "Baseball":

                # Query baseball stat tables
                cur.execute(PLAYER_HITTING_STATS_SQL, (game_id,))
                player_hitting_stats = cur.fetchall()

                cur.execute(PLAYER_PITCHING_STATS_SQL, (game_id,))
                player_pitching_stats = cur.fetchall()

                cur.execute(PLAYER_FIELDING_STATS_SQL, (game_id,))
                player_fielding_stats = cur.fetchall()

                context.update(
                    player_hitting_stats=player_hitting_stats,
                    player_pitching_stats=player_pitching_stats,
                    player_fielding_stats=player_fielding_stats,
                )

                template_name = "game_detail/baseball.html"

            if sport_name == "Football":

                cur.execute(PLAYER_FOOTBALL_OFFENSE_STATS_SQL, (game_id,))
                player_football_offense_stats = cur.fetchall()

                cur.execute(PLAYER_FOOTBALL_DEFENSE_STATS_SQL, (game_id,))
                player_football_defense_stats = cur.fetchall()

                context.update(
                    player_football_offense_stats=player_football_offense_stats,
                    player_football_defense_stats=player_football_defense_stats,
                )

                template_name = "game_detail/football.html"

           
            return render_template(template_name, **context)
    finally:
        conn.close()

    




    