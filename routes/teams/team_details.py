from .. import routes_bp
from flask import redirect, url_for, render_template
from core.get_db_connection import get_db_connection
from psycopg2.extras import RealDictCursor





@routes_bp.route("/teams/<team_slug>")
def team_detail(team_slug: str):
    team_sql = """
    SELECT 
    t.site_slug AS slug,
    CONCAT(t.school_name, ' ', s.name) AS name
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    WHERE t.site_slug = %s
    LIMIT 1;
    """

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(team_sql, (team_slug,))
            team = cur.fetchone()


    finally:
        conn.close()

    
    
    SAMPLE_EVENTS = [
        {"id": 1, "date": "2025-10-08", "sport": "Football", "title": "Tigers vs Wildcats", "location": "Memorial Stadium"},
        {"id": 2, "date": "2025-10-10", "sport": "Basketball", "title": "Tigers vs Bears", "location": "Mizzou Arena"},
        {"id": 3, "date": "2025-10-12", "sport": "Soccer", "title": "Tigers vs Lions", "location": "Walton Stadium"},
        {"id": 4, "date": "2025-10-15", "sport": "Baseball", "title": "Tigers vs Hawks", "location": "Taylor Stadium"},
    ]
    team_events = SAMPLE_EVENTS  # keep placeholder logic

    news = [
        
    ]
    

    return render_template("team_detail.html", team=team, events=team_events, news=news)