from flask import Blueprint

routes_bp = Blueprint("routes", __name__)

from .home import *
from .news import *
from .players import *
from .scores import *
from .teams import *
from .user import *