from flask import Blueprint

routes_bp = Blueprint("routes", __name__)

from .home.home import *
from .home.search import *
from .news.news import *
from .players.players import *
from .players.player_detail_baseball import *
from .scores.scores import *
from .scores.game_detail import *
from .teams.teams import *
from .teams.team_details import *
from .teams.team_roster import *
from .user.profile import *