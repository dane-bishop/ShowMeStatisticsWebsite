from .. import routes_bp
from flask import redirect, render_template, url_for
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor
from routes.scores.game_detail_queries.game import GAME_SQL
from routes.scores.game_detail_queries.player_hitting import PLAYER_HITTING_STATS_SQL
from routes.scores.game_detail_queries.player_pitching import PLAYER_PITCHING_STATS_SQL
from routes.scores.game_detail_queries.player_fielding import PLAYER_FIELDING_STATS_SQL
from routes.scores.game_detail_queries.player_football_offense import PLAYER_FOOTBALL_OFFENSE_STATS_SQL
from routes.scores.game_detail_queries.player_football_defense import PLAYER_FOOTBALL_DEFENSE_STATS_SQL
from routes.scores.game_detail_queries.player_basketball import PLAYER_BASKETBALL_STATS_SQL



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


            # IF SPORT IS BASEBALL
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



            # IF SPORT IS FOOTBALL
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





            # IF SPORT IS BASKETBALL
            if sport_name == "Men's Basketball" or sport_name == "Women's Basketball":

                cur.execute(PLAYER_BASKETBALL_STATS_SQL, (game_id,))
                player_basketball_stats = cur.fetchall()


                context.update(
                    player_basketball_stats=player_basketball_stats,
                )

                template_name = "game_detail/basketball.html"
                




           
            return render_template(template_name, **context)
    finally:
        conn.close()

    




    