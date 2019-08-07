from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *
import re
from word_filter import *

BP = Blueprint('admin', __name__)

UPLOAD_IMG_PATH = "/static/image/"
IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

ACCESS_DENIED_TAG = {'ADMIN', '갤러리', '공모전', '공지', '블랙리스트', '비밀글', '대외활동', '외부사이트', '장부', '취업', '학생회소개'}
ACCESS_DENIED_BOARD = ['공지', '갤러리', '학생회소개', '통계', '대외활동', '대외활동_공모전', '대외활동_취업', '투표', '장부']
#######################################################
#페이지 URL#############################################
@BP.route('/settings')
def settings():
	today = select_today_visitor(g.db)

	if request.remote_addr not in today:
		#방문자 기록
		insert_today_visitor(g.db, request.remote_addr)

	return render_template('admin/settings.html')
#######################################################
#관리자 기능#############################################

#게시판 추가/수정 (OK)
@BP.route('/board_upload', methods=['POST'])
@jwt_required
def board_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	boards_str = request.form['boards']

	boards_replace = boards_str.replace("'", "\"")
	boards = json.loads(boards_replace)

	#전송받은 board_url 리스트들
	board_url_list = []
	for board in boards:
		check = re.compile('[^ ㄱ-ㅣ가-힣|a-z|0-9|_]+').sub('', board['board_url'])

		#길이가 달라졌다?! = 특수문자 들어간거임
		if len(board['board_url']) != len(check):
			return jsonify(result = "do not use special characters")

		board_url_list.append(board['board_url'])

	#필수 board_url 체크
	check_board = list(set(ACCESS_DENIED_BOARD) - set(board_url_list))

	#만약 필수 보드가 체크보드에 남아있다면?
	if len(check_board) > 0:
		return jsonify(
			result = "fail",
			necessary_board = check_board)

	#필수 보드가 다 포함이라면?
	else:
		result = update_boards(g.db, boards)
		return jsonify(result = result)

###############################################
#여기는 우선 만들어둠.
#정적변수 테이블을 (추가 / 삭제)는 사실상 관리자가 쓸 일이 없을 것 같음.

#정적 variable 추가
@BP.route('/variable_upload', methods=['POST'])
@jwt_required
def variable_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	key = request.form['key']
	value = request.form['value']

	#욕 필터
	if check_word_filter(key):
		return jsonify(result = "unavailable word")
	if check_word_filter(value):
		return jsonify(result = "unavailable word")

	result = insert_variable(g.db, key, value)

	return jsonify(
		result = result)

#정적 variable 삭제
@BP.route('/variable_delete', methods=['POST'])
@jwt_required
def variable_delete():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	key = request.form['key']

	result = delete_variable(g.db, key)

	return jsonify(
		result = result)
###############################################

#정적 variable 리스트 반환 (OK)
@BP.route('/get_variables')
def get_variables():
	result = {}

	variables = select_variables(g.db)

	result.update(
		variables = variables,
		result = "success")

	return jsonify(result)

#정적 variable 단일 반환 (OK)
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

#정적 variable 값 변경 (OK)
@BP.route('/variable_update', methods=['POST'])
@jwt_required
def variable_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	key = request.form['key']
	value = request.form['value']

	#욕 필터
	if check_word_filter(key):
		return jsonify(result = "unavailable word")
	if check_word_filter(value):
		return jsonify(result = "unavailable word")

	result = update_variable(g.db, key, value)

	return jsonify(result = result)

#학생회 로고 변경 (로고는 이미지를 받아야하니 정적변수 수정을 따로 구현) (OK)
@BP.route('/change_logo', methods=['POST'])
@jwt_required
def change_logp():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	#이미지를 받는다.
	img = request.files['img']
	
	#확장자 및 파일이름길이 확인.
	if secure_filename(img.filename).split('.')[-1] in IMG_EXTENSIONS and len(img.filename) < 240:

		#파일이름 변경.
		img_name = str(datetime.today().strftime("%Y%m%d%H%M%S%f")) + '_Modakbullogo_' + img.filename

		#변경된 파일이름 학생회 로고 변수에 저장.
		result = update_variable(g.db, "학생회로고", img_name)

		#디비 저장 성공이면,
		if result == "success":
			#파일 저장
			img.save('.' + UPLOAD_IMG_PATH + img_name)
		else:
			return jsonify(result = "file save fail")
	else:
		return jsonify(result = "wrong extension")

	return jsonify(result = "success")

#부서 반환 (OK)
@BP.route('/get_department/<int:dm_type>')
def get_department(dm_type):
	result = {}

	department = select_department_type(g.db, dm_type)

	result.update(
		department = department,
		result = "success")

	return jsonify(result)

#부서 추가 / 수정 (프론트 구조상) (OK)
@BP.route('/department_update', methods=['POST'])
@jwt_required
def department_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	dm_id = request.form['dm_id']
	dm_name = request.form['dm_name']
	dm_chairman = request.form['dm_chairman']
	dm_intro = request.form['dm_intro']
	dm_type = request.form['dm_type']
	dm_img = request.files.getlist('dm_img')

	#욕 필터
	if check_word_filter(dm_name):
		return jsonify(result = "unavailable word")
	if check_word_filter(dm_chairman):
		return jsonify(result = "unavailable word")
	if check_word_filter(dm_intro):
		return jsonify(result = "unavailable word")

	if dm_img:
		dm_img = dm_img[0]
		#확장자 및 파일이름길이 확인.
		if secure_filename(dm_img.filename).split('.')[-1] in IMG_EXTENSIONS and len(dm_img.filename) < 240:
			#파일이름 변경.
			img_name = str(datetime.today().strftime("%Y%m%d%H%M%S%f")) + '_dm_img_' + dm_img.filename

			#이게 있는 부서인지 확이 후, 있으면 update / 없으면 insert (프론트 구조상 통합)
			if select_department_id(g.db, dm_id) is not None:
				result = update_department(g.db, dm_id, dm_name, dm_chairman, dm_intro, img_name, dm_type)
			else:
				result = insert_department(g.db, dm_id, dm_name, dm_chairman, dm_intro, img_name, dm_type)

			#디비 저장 성공이면,
			if result == "success":
				#파일 저장
				dm_img.save('.' + UPLOAD_IMG_PATH + img_name)
			else:
				return jsonify(result = "file save fail")
		else:
			return jsonify(result = "wrong extension")

	else:
		#이게 있는 부서인지 확이 후, 있으면 update / 없으면 insert (프론트 구조상 통합)
		if select_department_id(g.db, dm_id) is not None:
			result = update_department_noneimg(g.db, dm_id, dm_name, dm_chairman, dm_intro, dm_type)
		else:
			result = "img is not defined"

	return jsonify(result = result)

#부서 삭제 (OK)
@BP.route('/department_delete/<int:dm_id>')
@jwt_required
def department_delete(dm_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	#삭제할 부서가 DB에 있나 확인
	if select_department_id(g.db, dm_id) is None:
		result = "department is not defined"

	result = delete_department(g.db, dm_id)

	return jsonify(
		result = result)

#태그 목록 반환 (OK)
@BP.route('/get_tags')
@jwt_required
def get_tags():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = {}

	tags = select_tags(g.db)

	tag_list = []
	for tag in tags:
		if tag['tag_id'] != "ADMIN":
			tag_list.append(tag['tag_id'])

	result.update(
		result = "success",
		tags = tag_list)

	return jsonify(result)

#태그 목록 반환 (수정 / 삭제 불가능한 태그들은 제외한 리스트) (OK)
@BP.route('/get_access_tags')
@jwt_required
def get_access_tags():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = {}

	tags = select_tags(g.db)

	tag_list = []
	for tag in tags:
		if tag['tag_id'] not in ACCESS_DENIED_TAG:
			tag_list.append(tag['tag_id'])

	result.update(
		result = "success",
		tags = tag_list)

	return jsonify(result)

#태그 추가 (OK)
@BP.route('/input_tag', methods=['POST'])
@jwt_required
def input_tag():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	tag = request.form['tag']

	#욕 필터#
	if check_word_filter(tag):
		return jsonify(result = "unavailable word")

	check = re.compile('[^ ㄱ-ㅣ가-힣|a-z|0-9]+').sub('', tag)

	#길이가 달라졌다?! = 특수문자 들어간거임
	if len(tag) != len(check):
		return jsonify(result = "do not use special characters")

	#해당 태그가 DB에 없으면?
	if check_tag(g.db, tag) is not None:
		insert_tag(g.db, tag)
		result = "success"
	else:
		result = "already tag"

	return jsonify(result = result)

#태그 삭제 (OK)
@BP.route('/delete_tag', methods=['POST'])
@jwt_required
def delete_tag_():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	tag = request.form['tag']

	#이 접근 불가 태그 검사
	if tag in ACCESS_DENIED_TAG: abort(400)

	if check_tag(g.db, tag) is None:
		result = "tag is not define"
	else:
		result = delete_tag(g.db, tag)

	return jsonify(result = result)

#태그명 수정 (OK)
@BP.route('/update_tag', methods=['POST'])
@jwt_required
def update_tag_():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	old_tag = request.form['old_tag']
	new_tag = request.form['new_tag']

	#욕 필터
	if check_word_filter(new_tag):
		return jsonify(result = "unavailable word")

	check = re.compile('[^ ㄱ-ㅣ가-힣|a-z|0-9]+').sub('', new_tag)

	#길이가 달라졌다?! = 특수문자 들어간거임
	if len(new_tag) != len(check):
		return jsonify(result = "do not use special characters")

	#접근 불가 태그 검사
	if old_tag in ACCESS_DENIED_TAG: abort(400)

	if check_tag(g.db, old_tag) is None:
		result = "tag is not define"
	else:
		result = update_tag(g.db, old_tag, new_tag)

	return jsonify(result = result)

#로그 검색 (미사용)
@BP.route('/search_log', methods=['POST'])
@jwt_required
def search_log():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)
	
	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = {}
	
	input_str = request.form['input_str']

	topic_list = input_str.split('_')

	result_log = select_log(g.db, topic_list)

	result.update(
		result = "success",
		result_log = result_log)

	return jsonify(result)

#총 회원 반환 (OK)
@BP.route('/get_user_list')
@jwt_required
def get_user_list():
	result = {}
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정 확인
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	user_list = select_user_list(g.db)

	for user in user_list:
		tags = select_user_tag(g.db, user['user_id'])
		user.update(user_tags = tags)

	return jsonify(
		result = "success",
		user_list = user_list)

#특정 회원 반환 (OK)
@BP.route('/get_user_search', methods=['POST'])
@jwt_required
def get_user_search():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 계정이 아니면 ㅃ2
	if not check_admin(g.db, user['user_id']):
		return jsonify(result = "you are not admin")

	search = request.form['search']

	user_list = select_user_search(g.db, search)

	if user is None:
		return jsonify(result = "user is not defined")

	for user in user_list:
		tags = select_user_tag(g.db, user['user_id'])
		user.update(tags = tags)

	return jsonify(
		result = "success",
		user = user_list)

#블랙리스트 반환 (OK)
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

	blacklist = select_user_tag_search(g.db, '블랙리스트')

	for user in blacklist:
		tags = select_user_tag(g.db, user['user_id'])
		user.update(tags = tags)

	return jsonify(
		blacklist = blacklist,
		result = "success")

#블랙리스트 등록 (OK)
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

	#이미 블랙인지 확인
	target_tags = select_user_tag(g.db, target['user_id'])
	if '블랙리스트' in target_tags:
		return jsonify(result = "already blacklist")

	result = insert_user_tag(g.db, target['user_id'], "블랙리스트")

	return jsonify(
		result = result)

#블랙리스트 해지 (OK)
@BP.route('/user_black_cancel', methods=['POST'])
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

	target_tags = select_user_tag(g.db, target['user_id'])
	if '블랙리스트' not in target_tags:
		return jsonify(result = "no blacklist")

	result = delete_user_tag(g.db, target['user_id'], "블랙리스트")

	return jsonify(
		result = result)

#관리자 비밀번호 변경 (OK)
@BP.route('/change_pw', methods=['POST'])
@jwt_required
def change_pw():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)
	
	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	old_pw = request.form['old_pw']
	new_pw_1 = request.form['new_pw_1']
	new_pw_2 = request.form['new_pw_2']

	if new_pw_1 != new_pw_2:
		return jsonify(result = "not same pw")

	if check_password_hash(user['pw'], old_pw):
		result = update_user_pw(g.db, user['user_id'], generate_password_hash(new_pw_1))
	else:
		result = "wrong old pw"

	return jsonify(result = result)
