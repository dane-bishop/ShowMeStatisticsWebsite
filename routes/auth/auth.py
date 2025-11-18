from . import auth_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor
from core.get_db_connection import get_db_connection



class User(UserMixin):
    def __init__(self, id, email, password_hash, display_name, is_active, created_at, updated_at):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.display_name = display_name
        self._is_active = bool(is_active)  # ensure bool
        self.created_at = created_at
        self.updated_at = updated_at

        @property
        def is_active(self) -> bool:          # <-- override the read-only property
            return self._is_active



def _row_to_user(row):
    if not row:
        return None
    # Prefer .get("...") for nullable fields; [] for required fields
    return User(
        id=row["id"],
        email=row["email"],
        password_hash=row.get("password_hash"),
        display_name=row.get("display_name"),
        # support either column name
        is_active=row.get("is_active"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


def load_user_by_id(user_id: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, email, display_name, is_active FROM users WHERE id = %s", (user_id,))
            return _row_to_user(cur.fetchone())
    finally:
        conn.close()


# ----- Routers -------
@auth_bp.get("/register")
def register_form():
    if getattr(current_user, "is_authenticated", False):
        return redirect(url_for("routes.home"))  # or wherever
    return render_template("auth/register.html")


@auth_bp.post("/register")
def register_submit():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    username = (request.form.get("username") or "").strip() or None

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for("auth.register_form"))

    pw_hash = generate_password_hash(password)

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO users (email, password_hash, display_name)
                    VALUES (%s, %s, %s)
                    RETURNING id, email, display_name, is_active
                """, (email, pw_hash, username))
                urow = cur.fetchone()
        user = _row_to_user(urow)
        login_user(user)
        flash("Welcome! Your account has been created.", "success")
        return redirect(url_for("routes.home"))  # or account page
    except Exception as e:
        # Most common: duplicate email
        flash("Could not create account (email in use?).", "error")
        return redirect(url_for("auth.register_form"))
    finally:
        conn.close()




@auth_bp.get("/login")
def login_form():
    if getattr(current_user, "is_authenticated", False):
        return redirect(url_for("routes.home"))
    return render_template("auth/login.html")



@auth_bp.post("/login")
def login_submit():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, email, password_hash, display_name, is_active FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
        if not row or not check_password_hash(row["password_hash"], password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login_form"))
        user = _row_to_user(row)
        if not user.is_active:
            flash("This account is disabled.", "error")
            return redirect(url_for("auth.login_form"))
        login_user(user, remember=True)
        flash("Signed in.", "success")
        return redirect(url_for("routes.home"))
    finally:
        conn.close()



@auth_bp.post("/logout")
@login_required
def logout_submit():
    logout_user()
    flash("Signed out.", "success")
    return redirect(url_for("routes.home"))