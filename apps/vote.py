from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

import json

BP = Blueprint('vote', __name__)

#######################################################
#페이지 URL#############################################

#######################################################
#투표 기능###############################################

#투표 업로드
@BP.route('/vote_upload', methods=['POST'])
@jwt_required
def vote_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	#보트 정보 불러오기 + json으로 변환 (아래와 같은 형식)
	vote_str = reqeust.form['vote']
	vote_replace = vote_str.replace("'", "\"")
	vote_json = json.loads(vote_replace)
	
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
	
	#유저 아이디 추가.
	vote_json.update(user_id = user['user_id'])

	result = insert_vote(g.db, vote_json)

	return jsonify(result = result)

#투표 하기
@BP.route('/vote_answer', methods=['POST'])
@jwt_required
def vote_answer():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 접근 거절!
	if check_admin(g.db, user['user_id']): 
		abort(400)

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
			"ans": [1]},

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

#투표 글들 불러오기(페이지네이션)
@BP.route('/get_votes')
def get_votes():
	result = {}

	votes = select_votes(g.db)

	for vote in votes:
		vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
		vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	return jsonify(
		result = "success",
		votes = votes)

#해당 투표 글 불러오기
@BP.route('/get_vote/<int:vote_id>')
def get_vote(vote_id):
	result = {}
	vote = select_vote(g.db, vote_id)

	if vote is None:
		return jsonify(reuslt = "define vote")

	ques = select_vote_que(g.db, vote_id)
	attach = select_vote_attach(g.db, vote_id)

	#프론트의 요구로 날짜 형식 변형
	vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
	vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	for que in ques:
		select = select_vote_select(g.db, que['que_id'])
		que.update(select = select)

	vote.update(que_list = ques)

	result.update(
		vote = vote,
		file = attach,
		result = "success")

	return result

#투표 마감기한 수정
@BP.route('/vote_update', methods=['POST'])
@jwt_required
def vote_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	end_date = reqeust.form['end_date']

	result = update_vote(user['user_id'], end_date)

	return jsonify(result = result)

#투표 삭제
@BP.route('/vote_delete/<int:vote_int>')
@jwt_required
def vote_delete(vote_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = delete_vote(g.db, vote_id, user['user_id'])

	return jsonify(result = result)


