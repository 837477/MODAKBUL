from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('vote', __name__)

@BP.route('/vote_upload')
#@jwt_required
def vote_upload():
	#user = select_user(g.db, get_jwt_identity())
	#if user is None: abort(400)

	#관리자 아니면 접근 거절!
	#if not check_admin(g.db, user['user_id']): 
		#abort(400)

	#Vote 메인 입력

	temp_vote = {
		"title": "투표제목.",
		"content": "내용입니다.",
		"end_date": "2019-08-20 17:30:00",
		"que": [
			{"question": "체크박스 질문1",
			"que_type": 0,
			"select": ["1답안", "2답안", "3답안"]},
			{"question": "라디오 질문2",
			"que_type": 1,
			"select": ["1답안", "2답안"]},
			{"question": "단답형 질문3",
			"que_type": 2,
			}]
		}

	temp_vote.update(user_id = "16011092")

	result = insert_vote(g.db, temp_vote)

	print(result)

	return jsonify(result = result)


