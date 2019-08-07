from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *
from word_filter import *

import json

BP = Blueprint('vote', __name__)
UPLOAD_PATH = "/static/files/"
IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
#######################################################
#페이지 URL#############################################
@BP.route('/vote')
def vote():
   return render_template('vote/vote.html')
#######################################################
#투표 기능###############################################

#투표 업로드 (OK)
@BP.route('/vote_upload', methods=['POST'])
@jwt_required
def vote_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		return jsonify(result = "you are not admin")

	#보트 정보 불러오기 + json으로 변환 (아래와 같은 형식)
	vote_str = request.form['vote']
	file = request.files.getlist('file')

	#욕 필터
	if check_word_filter(vote_str):
		return jsonify(result = "unavailable word")

	vote_replace = vote_str.replace("'", "\"")
	vote_json = json.loads(vote_replace)

	#유저 아이디 추가.
	vote_json.update(user_id = user['user_id'])

	#파일이 있냐?!
	if file:
		file = file[0]

		#파일 확장자 / 이름길이 체크
		file_check = file_name_encode(file.filename)

		if file_check is not None:
			#DB에 투표글 추가!
			result = insert_vote(g.db, vote_json, file_check)

			if result == "success":
				file.save('.' + UPLOAD_PATH + file_check)
			else:
				return jsonify(result = "fail")
		else:
			return jsonify(result = "wrong file")	

	#파일이 없다!
	else:
		result = insert_vote(g.db, vote_json, None)

	return jsonify(
		result=result)

	'''
	vote_json = {
		"title": "55)투표제목.",
		"content": "55)내용입니다.",
		"end_date": "2019-08-20 17:30:00",
		"que_list": [
			{"que": "55)체크박스 질문1",
			"que_type": 0,
			"select": ["55)1답안", "55)2답안", "55)3답안"]},
			{"que": "55)라디오 질문2",
			"que_type": 1,
			"select": ["55)1답안", "55)2답안"]},
			{"que": "55)단답형 질문3",
			"que_type": 2,
			}]
		}
	'''

#투표 하기 (OK)
@BP.route('/vote_answer', methods=['POST'])
@jwt_required
def vote_answer():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 접근 거절!
	if check_admin(g.db, user['user_id']): 
		return jsonify(result = "admin can not vote")

	#질의응답 정보 불러오기 + json으로 변환 (아래와 같은 형식)
	answer_str = request.form['answer']
	answer_replace = answer_str.replace("'", "\"")
	answer_json = json.loads(answer_replace)

	'''
	answer_json = {
		"vote_id": 1,
		"ans_list": [
			{"que_id": 1,
			"que_type": 0,
			"ans": [1, 2]},

			{"que_id": 2,
			"que_type": 1,
			"ans": [3]},

			{"que_id": 3,
			"que_type": 2,
			"ans": "단답형"}]
		}
	'''

	#투표 중복 체크
	if check_already_vote(g.db, answer_json['vote_id'], user['user_id']) == 1:
		return jsonify(result = "already_vote")

	#유저 아이디 추가.
	answer_json.update(user_id = user['user_id'])

	result = insert_vote_user_answer(g.db, answer_json)

	return jsonify(result = result)

#투표 목록 불러오기 (OK)
@BP.route('/get_votes')
def get_votes():
	votes = select_votes(g.db)

	for vote in votes:
		vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
		vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	return jsonify(
		result = "success",
		votes = votes)

#특정 투표 글 불러오기 (OK)
@BP.route('/get_vote/<int:vote_id>')
def get_vote(vote_id):
	result = {}
	vote = select_vote(g.db, vote_id)

	if vote is None:
		return jsonify(reuslt = "define vote")

	ques = select_vote_que(g.db, vote_id)

	#프론트의 요구로 날짜 형식 변형
	vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
	vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	for que in ques:
		select = select_vote_select(g.db, que['que_id'])
		que.update(select = select)

	vote.update(que_list = ques)

	result.update(
		vote = vote,
		result = "success")

	return jsonify(result)

#투표 삭제 (OK)
@BP.route('/vote_delete/<int:vote_id>')
@jwt_required
def vote_delete(vote_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)
	
	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = delete_vote(g.db, vote_id, user['user_id'])

	return jsonify(result = result)

#투표 마감기한 수정 (미사용 중)
@BP.route('/vote_update', methods=['POST'])
@jwt_required
def vote_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	end_date = reqeust.form['end_date']

	result = update_vote(user['user_id'], end_date)

	return jsonify(result = result)

#######################################################
#함수 ##################################################
def file_name_encode(file_name):
	#허용 확장자 / 길이인지 확인.
	if secure_filename(file_name).split('.')[-1].lower() in IMG_EXTENSIONS and len(file_name) < 240:

		#이름 변환!
		path_name = str(datetime.today().strftime("%Y%m%d%H%M%S%f")) + '_' + file_name

		return path_name
	
	else:
		return None


