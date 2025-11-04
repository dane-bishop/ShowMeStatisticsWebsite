from flask import Blueprint
favorites_bp = Blueprint("favorites", __name__, url_prefix="/favorites")
from .favorites import *