from .. import routes_bp
from flask import render_template, abort, url_for
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection
from flask_login import current_user


@routes_bp.route("/teams/<team_slug>/<int:team_year>/roster")
def team_roster(team_slug: str, team_year: int):
    TEAM_SQL = """
    SELECT
      t.id            AS team_id,
      t.school_name,
      t.site_slug,
      s.id            AS sport_id,
      s.name          AS sport_name
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    WHERE t.site_slug = %s
    """

    ROSTER_SQL = """
    SELECT
      p.id                           AS player_id,
      p.full_name,
      p.player_slug,

      rm.id                          AS roster_membership_id,
      rm.team_season_id,
      rm.jersey,
      rm.position,
      rm.class_year,
      rm.height_raw,
      rm.weight_lbs,
      rm.bats_throws,
      rm.hometown,
      rm.high_school,

      ts.id                          AS team_season_id,
      ts.team_id                     AS ts_team_id,
      ts.year                        AS season_year,

      t.id                           AS t_id,
      t.sport_id                     AS t_sport_id,

      s.id                           AS s_id,
      s.name                         AS sport_name
    FROM roster_memberships rm
    JOIN players       p  ON p.id  = rm.player_id
    JOIN team_seasons  ts ON ts.id = rm.team_season_id
    JOIN teams         t  ON t.id  = ts.team_id
    JOIN sports        s  ON s.id  = t.sport_id
    WHERE t.site_slug = %s
      AND ts.year = %s
      AND p.player_slug IS NOT NULL
      AND p.player_slug <> ''
    ORDER BY
      -- Try jersey numerical sort when numeric, otherwise by name
      (CASE WHEN rm.jersey ~ '^[0-9]+$' THEN rm.jersey::int END) NULLS LAST,
      p.full_name ASC;
    """

    FAVORITES_SQL = """
      SELECT entity_id
      FROM favorites
      WHERE user_id = %s
      AND entity_type = 'player'
    
    """

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