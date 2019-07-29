from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('admin', __name__)

#######################################################
#관리자 기능#############################################

#정적 variable 반환
@BP.route('/get_variable')
def get_variable():
	result = {}

	variable = select_variable(g.db)

	result.update(
		variable = variable,
		result = "success")

	return jsonify(result)

#정적 variable 추가
@BP.route('/variable_upload', methods=['POST'])
@jwt_required
def variable_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	key = request.form['key']
	value = request.form['value']

	result = insert_variable(g.db, key, value)

	return jsonify(
		result = result)


