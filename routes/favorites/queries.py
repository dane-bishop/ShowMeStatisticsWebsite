# routes/favorites/queries.py
from psycopg2.extras import RealDictCursor

def fetch_favorite_players(conn, user_id: int, limit: int = 24):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            WITH fav AS (
              SELECT entity_id, created_at
              FROM favorites
              WHERE user_id = %s AND entity_type = 'player'
              ORDER BY created_at DESC
              LIMIT %s
            ),
            rows AS (
              SELECT
                f.created_at,
                p.id              AS player_id,
                p.full_name,
                p.player_slug,
                t.school_name     AS team_name,
                rm.position,
                ts.year
              FROM fav f
              JOIN players p             ON p.id = f.entity_id
              JOIN roster_memberships rm ON rm.player_id = p.id
              JOIN team_seasons ts       ON ts.id = rm.team_season_id
              JOIN teams t               ON t.id = ts.team_id
            )
            SELECT DISTINCT ON (player_id)
                   player_id, full_name, player_slug, team_name, position, year, created_at
            FROM rows
            ORDER BY player_id, year DESC, created_at DESC;
        """, (int(user_id), int(limit)))
        return cur.fetchall()
