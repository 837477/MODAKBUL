from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('admin', __name__)

#######################################################
#관리자 기능#############################################

#정적 variable 리스트 반환
@BP.route('/get_variables')
def get_variables():
	result = {}

	variables = select_variables(g.db)

	result.update(
		variables = variables,
		result = "success")

	return jsonify(result)

#정적 variable 단일 반환
@BP.route('/get_value/<string:key>')
def get_value(key):
	result = {}

	value = select_value(g.db, key)

	if value is None:
		return jsonify(result = "define key")

	result.update(
		value = value['value'],
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

#정적 variable 삭제
@BP.route('/variable_delete', methods=['POST'])
@jwt_required
def variable_delete():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	key = request.form['key']

	result = delete_variable(g.db, key)

	return jsonify(
		result = result)

#부서 반환
@BP.route('/get_department')
def get_department():
	result = {}

	department = select_department(g.db)

	result.update(
		department = department,
		result = "success")

	return jsonify(result)

#부서 추가
@BP.route('/department_upload', methods=['POST'])
@jwt_required
def department_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	dm_name = request.form['dm_name']
	dm_chairman = request.form['dm_chairman']
	dm_intro = request.form['dm_intro']

	result = insert_department(g.db, dm_name, dm_chairman, dm_intro)

	return jsonify(
		result = result)



#부서 삭제
@BP.route('/department_delete', methods=['POST'])
@jwt_required
def department_delete():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	dm_id = request.form['dm_id']

	result = delete_department(g.db, dm_id)

	return jsonify(
		result = result)


