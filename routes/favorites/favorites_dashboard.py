from . import favorites_bp
from flask import jsonify, request, abort, render_template
from flask_login import login_required, current_user
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection


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