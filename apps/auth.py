from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from global_func import *
from sejong_account import sejong_api

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
	
	user = select_id(g.db, USER_ID)
	if user is None:
		sejong_api_result = sejong_api(USER_ID, USER_PW)
		if not sejong_api_result['result']:
			return jsonify(result = "You are not sejong")
		else:
			db_data = (
				int(USER_ID),
				generate_password_hash(USER_PW),
				sejong_api_result['name'],
				sejong_api_result['major'],
				sejong_api_result['name'],
				"1"
				)
			with g.db.cursor() as cursor:
				sql = open("database/auth_user_register.sql").read()
				cursor.execute(sql, db_data)
			g.db.commit()
	user = select_id(g.db, USER_ID)
	if check_password_hash(user['user_pw'], USER_PW):
		return jsonify(
			result = "success",
			access_token = create_access_token(identity = USER_ID, expires_delta=False)
			)
	else:
		return jsonify(result = "wrong info")

#회원정보 반환
@BP.route('/userinfo')
@jwt_required
def get_userinfo():
	user = select_id(g.db, get_jwt_identity())
	if user is None: abort(403)
	userinfo = {}
	with g.db.cursor() as cursor:
		#회원 정보 반환
		sql = "SELECT user_id, user_name, userr_major, user_nickname, user_access FROM user WHERE user_id = %s;"
		cursor.execute(sql, (user['user_id'],))
		userinfo.update(cursor.fetchone())
		#회원이 좋아요한 글 반환
		sql = "SELECT post_id FROM user_like WHERE user_id = %s;"
		cursor.execute(sql, (user['user_id'],))
		userinfo.update({"like_posts": cursor.fetchall()})
		#회원이 작성한 글 반환
		sql = "SELECT * FROM post WHERE user_id = %s;"
		cursor.execute(sql, (user['user_id'],))
		userinfo.update({"my_post": cursor.fetchall()})
		userinfo.update({"result":"success"})
	return jsonify(userinfo)

#닉네임 변경
@BP.route('/user_nickname_edit', methods=['POST'])
@jwt_required
def nickname_edit():
	new_nickname = request.form['new_nickname']
	user = select_id(g.db, get_jwt_identity())

	if user is None: abort(403)

	with g.db.cursor() as cursor:
		sql = "UPDATE user SET user_nickname=%s WHERE user_id=%s;"
		cursor.execute(sql, (new_nickname, user['user_id'],))
		g.db.commit()

###############################################
#사용자 관련 함수
def select_id(db, string):
	with db.cursor() as cursor: 
		sql = "SELECT * FROM user WHERE user_id = %s LIMIT 1"
		cursor.execute(sql, (string,))
		result = cursor.fetchone()
		return result

