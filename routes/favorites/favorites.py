from . import favorites_bp
from flask import jsonify, request, abort, render_template
from flask_login import login_required, current_user
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection

VALID_TYPES = {"player","team","game","stat_high"}


def _exists(conn, entity_type: str, entity_id: int) -> bool:
    # App-level referential check
    table = {
        "player": "players",
        "team": "teams",
        "game": "games",
        "stat_high": "player_season_highs"
    }[entity_type]
    pk = "id"
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table} WHERE {pk} = %s LIMIT 1", (entity_id,))
        return cur.fetchone() is not None
    

@favorites_bp.post("/toggle/<entity_type>/<int:entity_id>")
@login_required
def toggle_favorite(entity_type: str, entity_id: int):
    if entity_type not in VALID_TYPES:
        abort(400, "Invalid favorite type")
    conn = get_db_connection()
    try:
        with conn:
            if not _exists(conn, entity_type, entity_id):
                abort(404, "Entity not found")

            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id FROM favorites
                    WHERE user_id = %s AND entity_type = %s AND entity_id = %s
                """, (int(current_user.id), entity_type, entity_id))
                row = cur.fetchone()

                if row:
                    cur.execute("DELETE FROM favorites WHERE id = %s", (row["id"],))
                    return jsonify({"status": "unfavorited"})
                else:
                    cur.execute("""
                        INSERT INTO favorites (user_id, entity_type, entity_id)
                        VALUES (%s,%s,%s)
                        RETURNING id
                    """, (int(current_user.id), entity_type, entity_id))
                    _ = cur.fetchone()
                    return jsonify({"status": "favorited"})
                
    finally:
        conn.close()


@favorites_bp.get("/mine")
@login_required
def list_my_favorites():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT entity_type, entity_id, created_at
                FROM favorites
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 500
            """, (int(current_user.id),))
            return jsonify(cur.fetchall())
    finally:
        conn.close()


@favorites_bp.get("/dashboard")
@login_required
def favorites_dashboard():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT entity_type, entity_id, created_at
                FROM favorites
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 500
            """, (int(current_user.id),))
            favs = cur.fetchall()
        # You can split by type and bulk-fetch the rows to render.
        # For brevity, send favs to template and query there if you prefer.
        return render_template("favorites/dashboard.html", favorites=favs)
    finally:
        conn.close()
