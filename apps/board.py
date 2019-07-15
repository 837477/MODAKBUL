from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from global_func import *

bp = Blueprint('board', __name__)

