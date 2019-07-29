from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from db_func import *
from sejong_account import *

BP = Blueprint('auth', __name__)

###################################################
#페이지
@BP.route('/sign-in')
def sign_in():
	return render_template('auth/index.html')
###################################################

#로그인 및 회원가입(토큰발행) (OK)
@BP.route('/sign-in-up', methods=['POST'])
def login_modakbul():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']

	user = select_user(g.db, USER_ID)

	if user is None:
		sejong_api_result = dosejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			sejong_api_result = sejong_api(USER_ID, USER_PW)
			
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
		return jsonify(result = "incorrect password")

#회원정보 반환 (OK)
@BP.route('/get-userinfo')
@jwt_required
def get_userinfo():
	user = select_user(g.db, get_jwt_identity())
	#DB에 없는 유저임. 뭔가 이상하게 접근한 사람
	if user is None: abort(400)

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
@BP.route('/user-color', methods=['POST'])
@jwt_required
def user_color():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)
	new_color = request.form['new_color']
	result = change_user_color(g.db, user['user_id'], new_color)
	return jsonify(result = result)

#블랙리스트 등록
@BP.route('/user-black-apply', methods=['POST'])
@jwt_required
def user_black_apply():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

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
@BP.route('/user-black-cancle', methods=['POST'])
@jwt_required
def user_black_cancle():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

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



