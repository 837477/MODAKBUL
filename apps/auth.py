from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('auth', __name__)

###################################################
#페이지
@BP.route('/sign-in')
def sign_in():
	return render_template('auth/index.html')
###################################################

#로그인 및 회원가입(토큰발행)
@BP.route('/sign-in-up', methods=['POST'])
def login_modakbul():
	USER_ID = request.form['id']
	USER_PW = request.form['pw']
	
	user = select_user_id(g.db, USER_ID)
	
	if user is None:
		sejong_api_result = sejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			return jsonify(result = "You are not sejong")
		else:
			user_data = (
				USER_ID,
				generate_password_hash(USER_PW),
				sejong_api_result['name']
				)
			with g.db.cursor() as cursor:
				#user 테이블에 회원정보 추가
				sql = "INSERT INTO user(user_id, pw, user_name) VALUES (%s, %s, %s);"
				cursor.execute(sql, user_data)
				#user_tag 테이블에 학과태그 추가
				sql = "INSERT INTO user_tag(user_id, tag_id) VALUES (%s, %s);"
				cursor.execute(sql, (USER_ID, sejong_api_result['major'],))
			g.db.commit()
	user = select_user_id(g.db, USER_ID)
	
	if check_password_hash(user['pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(identity = USER_ID, expires_delta=False)
			)
	else:
		return jsonify(result = "incorrect password")

#회원정보 반환
@BP.route('/get-userinfo')
@jwt_required
def get_userinfo():
	user = select_user_id(g.db, get_jwt_identity())
	#DB에 없는 유저임. 뭔가 이상하게 접근한 사람
	if user is None: abort(400)

	user_tag = select_user_tag(g.db, user['user_id'])

	return jsonify(
		result = "success",
		user_id = user['user_id'],
		user_name = user['user_name'],
		user_color = user['user_color'],
		user_tag = user_tag)

#회원 컬러 변경
@BP.route('/user-color', methods=['POST'])
@jwt_required
def user_color():
	new_color = request.form['new_color']
	user = select_user_id(g.db, get_jwt_identity())

	if user is None: abort(400)

	change_user_colore(g.db, new_color, user['user_id'])
	
	return jsonify(result = "success")
	