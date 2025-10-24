from flask import Flask, render_template
from .. import routes_bp
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor



@routes_bp.route("/teams")
def teams():
    sql = """
    SELECT
        t.site_slug AS slug,
        CONCAT(t.school_name, ' ', s.name) AS name
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    ORDER BY name;
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    finally:
        conn.close()

    # Render with the same template + context shape as before:
    # each item has .name and .slug
    return render_template("teams.html", teams=rows)

