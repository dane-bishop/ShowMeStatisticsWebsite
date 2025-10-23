from .. import routes_bp
from flask import render_template


@routes_bp.route("/profile")
def profile():
    # Placeholder: not authenticated logic yet
    return render_template("profile.html", has_account=False)