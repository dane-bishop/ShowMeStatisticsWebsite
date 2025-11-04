# routes/profile.py
from .. import routes_bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from core.get_db_connection import get_db_connection

@routes_bp.get("/profile")
@login_required
def profile():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Pull basic user info
            cur.execute("""
                SELECT id, email, display_name, created_at
                FROM users
                WHERE id = %s
            """, (int(current_user.id),))
            user = cur.fetchone()

            # Pull a few recent favorites, grouped a bit
            cur.execute("""
                SELECT entity_type, entity_id, created_at
                FROM favorites
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 50
            """, (int(current_user.id),))
            favs = cur.fetchall() or []

        # Optional: pre-enrich some labels (example shows players/teams)
        # Do tiny lookups to name the entities (keep it simple & safe):
        players = [f["entity_id"] for f in favs if f["entity_type"] == "player"]
        teams   = [f["entity_id"] for f in favs if f["entity_type"] == "team"]

        labels = {"player": {}, "team": {}}
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if players:
                cur.execute(
                    "SELECT id, full_name FROM players WHERE id = ANY(%s)",
                    (players,))
                for r in cur.fetchall() or []:
                    labels["player"][r["id"]] = r["full_name"]

            if teams:
                cur.execute("""
                    SELECT t.id, CONCAT(t.school_name, ' ', s.name) AS label
                    FROM teams t
                    JOIN sports s ON s.id = t.sport_id
                    WHERE t.id = ANY(%s)
                """, (teams,))
                for r in cur.fetchall() or []:
                    labels["team"][r["id"]] = r["label"]

        return render_template("profile.html",
                               user=user,
                               favorites=favs,
                               labels=labels)
    finally:
        conn.close()


@routes_bp.post("/profile/display-name")
@login_required
def profile_update_display_name():
    display_name = (request.form.get("display_name") or "").strip() or None
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET display_name=%s, updated_at=now() WHERE id=%s",
                            (display_name, int(current_user.id)))
        flash("Display name updated.", "success")
    finally:
        conn.close()
    return redirect(url_for("routes.profile"))


@routes_bp.post("/profile/password")
@login_required
def profile_change_password():
    current_pw = request.form.get("current_password") or ""
    new_pw     = request.form.get("new_password") or ""
    if not new_pw:
        flash("New password is required.", "error")
        return redirect(url_for("routes.profile"))

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT password_hash FROM users WHERE id = %s", (int(current_user.id),))
            row = cur.fetchone()
            if not row or not check_password_hash(row["password_hash"], current_pw):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("routes.profile"))

        # Update with new hash
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET password_hash=%s, updated_at=now() WHERE id=%s",
                            (generate_password_hash(new_pw), int(current_user.id)))
        flash("Password updated.", "success")
    finally:
        conn.close()
    return redirect(url_for("routes.profile"))
