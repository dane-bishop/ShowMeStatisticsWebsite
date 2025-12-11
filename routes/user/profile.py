# routes/profile.py
from .. import routes_bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from core.get_db_connection import get_db_connection
from routes.favorites.queries import fetch_favorite_players


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

        fav_players = []
        if current_user.is_authenticated:
            fav_players = fetch_favorite_players(conn, current_user.id, limit=24)

        return render_template("profile.html",
                               user=user,
                               fav_players=fav_players)
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
                cur.execute(
                    "UPDATE users SET display_name=%s, updated_at=now() WHERE id=%s",
                    (display_name, int(current_user.id))
                )
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
                cur.execute(
                    "UPDATE users SET password_hash=%s, updated_at=now() WHERE id=%s",
                    (generate_password_hash(new_pw), int(current_user.id))
                )

        flash("Password updated.", "success")
    finally:
        conn.close()

    return redirect(url_for("routes.profile"))


# ----------------------------------------------------------------------
# Local-only demo route (no DB / no login)
# ----------------------------------------------------------------------
@routes_bp.get("/profile-demo")
def profile_demo():
    """
    This route lets you view the profile page without needing a database
    or logging in. Great for testing your CSS + avatar upload.
    """

    # Fake user object
    user = {
        "id": 999,
        "email": "demo@example.com",
        "display_name": "Demo User",
        "created_at": None,
    }

    # No DB → no favorites
    fav_players = []

    return render_template("profile.html", user=user, fav_players=fav_players)
