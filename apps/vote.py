from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

import json

BP = Blueprint('vote', __name__)

#투 글들 불러오기(페이지네이션) (OK)
@BP.route('/votes/<int:page>')
def get_vote(page):
	print("hi")

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
	temp_vote = {
		"title": "투표제목.",
		"content": "내용입니다.",
		"end_date": "2019-08-20 17:30:00",
		"que_list": [
			{"que": "체크박스 질문1",
			"que_type": 0,
			"select": ["1답안", "2답안", "3답안"]},
			{"que": "라디오 질문2",
			"que_type": 1,
			"select": ["1답안", "2답안"]},
			{"que": "단답형 질문3",
			"que_type": 2,
			}]
		}
	'''
	
	#유저 아이디 추가.
	vote_json.update(user_id = user['user_id'])

	result = insert_vote(g.db, vote_json)

	return jsonify(result = result)

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

#투표 하기
@BP.route('/vote_answer', methods=['POST'])
@jwt_required
def vote_answer():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#관리자 접근 거절!
	if check_admin(g.db, user['user_id']): 
		abort(400)
	'''
	temp_answer = {
		"vote_id": 1,
		"ans_list": [
			{"que_id": 1,
			"que_type": 0,
			"ans": []}]
		}
	'''
