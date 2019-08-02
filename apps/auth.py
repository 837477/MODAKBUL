from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from db_func import *
from sejong_account import *

BP = Blueprint('auth', __name__)

#######################################################
#페이지 URL#############################################
@BP.route('/sign-in')
def sign_in():
	return render_template('auth/index.html')

#######################################################
#회원 기능###############################################

#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign_in_up', methods=['POST'])
def login_modakbul():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = select_user(g.db, USER_ID)

	if user is None:
		sejong_api_result = dosejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			sejong_api_result = sejong_apßi(USER_ID, USER_PW)
			
		if not sejong_api_result['result']:
			return jsonify(result = "You are not sejong")
		else:
			user_data = (
				USER_ID,
				generate_password_hash(USER_PW),
				sejong_api_result['name']
				)
			insert_user(g.db, user_data, sejong_api_result['major'])

	user = select_user(g.db, USER_ID)
	
	#블랙리스트 인지 확인
	user_tag = select_user_tag(g.db, user['user_id'])
	if "블랙리스트" in user_tag:
		return jsonify(result = "blacklist")

	if check_password_hash(user['pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(identity = USER_ID, expires_delta=False)
			)
	else:
		#비번이 틀리면 우선 한번 더 sejong API 확인한다.
		sejong_api_result = dosejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			sejong_api_result = sejong_api(USER_ID, USER_PW)
			
		if not sejong_api_result['result']:
			return jsonify(result = "You are not sejong")
		else:
			#sejong API로 로그인에 성공하면, 세종 포털 비번변경으로 인한 로그인 실패.
			#DB비밀번호를 갱신시킨다.
			user = select_user(g.db, USER_ID)
			update_user_pw(g.db, user['user_id'], generate_password_hash(USER_PW))

			#블랙리스트 인지 확인
			user_tag = select_user_tag(g.db, user['user_id'])
			if "블랙리스트" in user_tag:
				return jsonify(result = "blacklist")

			if check_password_hash(user['pw'], USER_PW):
				return jsonify(
					result = "success",
					access_token = create_access_token(identity = USER_ID, expires_delta=False)
					)

#회원정보 반환 (OK)
@BP.route('/get_userinfo')
@jwt_required
def get_userinfo():
	user = select_user(g.db, get_jwt_identity())
	#DB에 없는 유저임. 뭔가 이상하게 접근한 사람
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	tags = select_user_tag(g.db, user['user_id'])

	if "블랙리스트" in tags:
		return jsonify(result = "blacklist")

	user_post_like = select_user_post_like(g.db, user['user_id'])
	user_comments = select_user_comments(g.db, user['user_id'])
	
	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_color = user['user_color'],
		user_tags = tags,
		user_like_posts = user_post_like,
		user_comments = user_comments)

#회원 컬러 변경 (OK)
@BP.route('/user_color', methods=['POST'])
@jwt_required
def user_color():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	new_color = request.form['new_color']
	result = change_user_color(g.db, user['user_id'], new_color)
	return jsonify(
		result = result)

#######################################################
#관리자 권한#############################################

#블랙리스트 반환
@BP.route('/get_blacklist')
@jwt_required
def get_blacklist():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정이 아니면 ㅃ2
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	result = select_user_tag_search(g.db, '블랙리스트')

	return jsonify(
		blacklist = result,
		result = "success")

#블랙리스트 등록
@BP.route('/user_black_apply', methods=['POST'])
@jwt_required
def user_black_apply():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정이 아니면 ㅃ2
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	target_id = request.form['target_id']

	target = select_user(g.db, target_id)
	if target is None:
		return jsonify(result = "no member")

	result = insert_user_tag(g.db, target['user_id'], "블랙리스트")

	return jsonify(
		result = result)

#블랙리스트 해지
@BP.route('/user_black_cancle', methods=['POST'])
@jwt_required
def user_black_cancle():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정이 아니면 ㅃ2
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	target_id = request.form['target_id']

	target = select_user(g.db, target_id)
	if target is None:
		return jsonify(result = "no member")

	result = delete_user_tag(g.db, target['user_id'], "블랙리스트")

	return jsonify(
		result = result)

#총 회원 반환
@BP.route('/get_user_list')
@jwt_required
def get_user_list():
	result = {}
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정이 아니면 ㅃ2
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	user_list = select_user_list(g.db)

	for user in user_list:
		tags = select_user_tag(g.db, user['user_id'])
		user.update(user_tags = tags)

	return jsonify(
		result = "result",
		user_list = user_list)

