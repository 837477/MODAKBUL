from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('admin', __name__)
