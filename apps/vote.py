from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('vote', __name__)

@BP.route('/vote_upload', methods = ['POST'])
@jwt_required
def vote_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	title = request.form['title']
	content = request.form['content']
	end_date = request.form['end_date']
	files = request.files.getlist('files')

	