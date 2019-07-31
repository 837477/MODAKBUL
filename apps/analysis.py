from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('analysis', __name__)

#누적 통계 반환
@BP.route('/today_analysis/<int:days>')
@jwt_optional
def visitor_analysis(days):
	result = {}

	#토큰이 있으면?
	if get_jwt_identity():
		user = select_user(g.db, get_jwt_identity())
		color = user['user_color']
	else:
		color = "#C30E2E"

	#기간 내 방문자 수 목록 반환
	everyday_analysis = select_everyday_analysis(g.db, days)

	#오늘 방문자 수 반환
	today_visitor = select_today_visitor_cnt(g.db)
	today = today_visitor['today_cnt']

	#전체 방문자 수 반환
	total_visitor = select_everyday_visitor_total(g.db)
	total = int(total_visitor['total'])

	result.update(
			user_color = color,
			everyday_analysis = everyday_analysis,
			today_visitor = today,
			total_visitor = total,
			result = "success")

	return jsonify(result)

#포스트 좋아요 랭킹 반환
@BP.route('/posts_like_rank/<int:days>')
def posts_like_rank(days):
	result = {}

	like_rank = select_posts_like_rank(g.db, days)

	result.update(
		result = "success",
		posts_like_rank = like_rank)

	return jsonify(result)

#포스트 조회수 랭킹 반환
@BP.route('/posts_view_rank/<int:days>')
def posts_view_rank():
	result = {}

	view_rank = select_posts_view_rank(g.db)

	result.update(
		result = "success",
		posts_view_rank = view_rank)

	return jsonify(result)

