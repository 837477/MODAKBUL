from flask import Blueprint, render_template, request, jsonifiy, g
from werkzeug.security import check_password_hash, generate_password_hash
from falsk_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sejong_account

BP = Blueprint('auth', __name__)

###################################################
#페이지
 @BP.route('/sign-in')
 def sign_in():
 	return render_template('auth/sign_in.html')

 @BP.route('/sign-up')
 def sign_up():
 	return render_template('auth/sign_up.html')
 ###################################################

#로그인 및 회원가입(토큰발행)
@BP.route('/sign_in_or_up', methods=['POST'])
def login_modakbul():
	ID = request.form['id']
	PW = request.form['pw']
	
	user = select_id(g.db, user_id)
	if user is None:
		sejong_api_result = sejong_api(ID, PW)

		if not sejong_api_result['result']:
			return jsonifiy(result = "You are not sejong")
		else:
			db_data = (
				int(ID)
				)