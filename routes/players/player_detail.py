from .. import routes_bp
from flask import render_template, abort, request, url_for
from psycopg2.extras import RealDictCursor
import psycopg2
from core.get_db_connection import get_db_connection
from flask_login import current_user
from routes.players.player_detail_queries.baseball.player import PLAYER_SQL
from routes.players.player_detail_queries.baseball.season_highs import SEASON_HIGHS_SQL
from routes.players.player_detail_queries.baseball.gamelog_hitting import GAMELOG_HITTING_SQL
from routes.players.player_detail_queries.baseball.gamelog_pitching import GAMELOG_PITCHING_SQL
from routes.players.player_detail_queries.baseball.gamelog_fielding import GAMELOG_FIELDING_SQL
from routes.players.player_detail_queries.baseball.favorites import IS_FAVORITE_SQL
from routes.players.player_detail_queries.football.player_football_offense import GAMELOG_FOOTBALL_OFFENSE_SQL
from routes.players.player_detail_queries.football.player_football_defense import GAMELOG_FOOTBALL_DEFENSE_SQL
from routes.players.player_detail_queries.basketball.player_basketball import GAMELOG_BASKETBALL_SQL
from routes.players.player_detail_queries.volleyball.player_volleyball import GAMELOG_VOLLEYBALL_SQL






@routes_bp.route("/players/<player_slug>")
def player_detail(player_slug: str):

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


            context = {
                "player": player,
                "highs": highs,
                "is_favorited": is_favorited,
                "back_url": back_url,
            }


            sport_name = (player.get("sport_name"))



            # BASEBALL

            if sport_name == "Baseball":

                # Game log hitting
                cur.execute(GAMELOG_HITTING_SQL, (player["id"],))
                gamelog_hitting = cur.fetchall()


                # Game log pitching
                cur.execute(GAMELOG_PITCHING_SQL, (player["id"],))
                gamelog_pitching = cur.fetchall()


                # Game log fielding
                cur.execute(GAMELOG_FIELDING_SQL, (player["id"],))
                gamelog_fielding = cur.fetchall()

                context.update(
                    gamelog_hitting=gamelog_hitting,
                    gamelog_pitching=gamelog_pitching,
                    gamelog_fielding=gamelog_fielding
                )

                template_name = "player_detail/baseball.html"




            # FOOTBALL
            
            if sport_name == "Football":

                # Game log offense
                cur.execute(GAMELOG_FOOTBALL_OFFENSE_SQL, (player["id"],))
                gamelog_football_offense = cur.fetchall()

                # Game log defense
                cur.execute(GAMELOG_FOOTBALL_DEFENSE_SQL, (player["id"],))
                gamelog_football_defense = cur.fetchall()

                context.update(
                    gamelog_football_offense=gamelog_football_offense,
                    gamelog_football_defense=gamelog_football_defense,
                )

                template_name = "player_detail/football.html"




            # BASKETBALL

            if sport_name == "Men's Basketball" or sport_name == "Women's Basketball":

                # Game log offense
                cur.execute(GAMELOG_BASKETBALL_SQL, (player["id"],))
                gamelog_basketball = cur.fetchall()


                context.update(
                    gamelog_basketball=gamelog_basketball,
                )

                template_name = "player_detail/basketball.html"





            # VOLLEYBALL

            if sport_name == "Women's Volleyball":

                # Game log offense
                cur.execute(GAMELOG_VOLLEYBALL_SQL, (player["id"],))
                gamelog_volleyball = cur.fetchall()


                context.update(
                    gamelog_volleyball=gamelog_volleyball,
                )

                template_name = "player_detail/volleyball.html"


        return render_template(template_name, **context)
    
    finally:
        conn.close()

    