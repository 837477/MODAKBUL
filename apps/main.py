from flask import *
from db_func import *

BP = Blueprint('main', __name__)

@BP.route('/')
def main_home():
	today = select_today_visitor(g.db)

	if request.remote_addr not in today:
		#방문자 기록
		insert_today_visitor(g.db, request.remote_addr)
	
	return render_template('main/index.html')