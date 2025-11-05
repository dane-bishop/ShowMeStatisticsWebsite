from flask import Blueprint
favorites_bp = Blueprint("favorites", __name__, url_prefix="/favorites")
from .queries import *
from .list_my_favorites import *
from .toggle_favorite import *