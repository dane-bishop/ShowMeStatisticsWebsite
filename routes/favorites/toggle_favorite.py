from . import favorites_bp
from flask import jsonify, request, abort, render_template
from flask_login import login_required, current_user
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection
from .helpers.exists import _exists
from psycopg2 import errors

VALID_TYPES = {"player","team","game","stat_high"}


@favorites_bp.post("/toggle")
@login_required
def toggle_favorite():
    data = request.get_json(silent=True) or {}
    entity_type = (data.get("type") or "").strip()
    entity_id   = data.get("id")

    if entity_type not in VALID_TYPES or not isinstance(entity_id, int):
        abort(400, "Invalid favorite payload")

    conn = get_db_connection()
    try:
        with conn:
            if not _exists(conn, entity_type, entity_id):
                abort(404, "Entity not found")

            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id 
                    FROM favorites
                    WHERE user_id = %s AND entity_type = %s AND entity_id = %s
                    FOR UPDATE
                """, (int(current_user.id), entity_type, entity_id))
                row = cur.fetchone()

                if row:
                    cur.execute("DELETE FROM favorites WHERE id = %s", (row["id"],))
                    return jsonify({"favorited": False})
                
                try:
                    cur.execute("""
                        INSERT INTO favorites (user_id, entity_type, entity_id)
                        VALUES (%s,%s,%s)
                        RETURNING id
                    """, (int(current_user.id), entity_type, entity_id))
                    cur.fetchone()
                    return jsonify({"favorited": True})
                except errors.UniqueViolation:
                    # Another concurrent tx inserted after our SELECT; treat as favorited
                    conn.rollback()      # rollback the failed statement
                    return jsonify({"favorited": True})
    finally:
        conn.close()