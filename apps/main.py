from flask import *
from db_func import *

BP = Blueprint('main', __name__)
#######################################################
#페이지 URL#############################################
@BP.route('/')
def main_home():
	today = select_today_visitor(g.db)

	if request.remote_addr not in today:
		#방문자 기록
		insert_today_visitor(g.db, request.remote_addr)
	
	return render_template('main/landing.html')

@BP.route('/credit')
def credit():
	return render_template('main/credit.html')
