from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('analysis', __name__)

#유저 방문자 수 반환
@BP.route('/visitor_analysis/<int:days>')
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
	visitor_cnt_list = select_everyday_visitor(g.db, days)

	#전체 방문자 수 반환
	total_visitor = select_everyday_visitor_total(g.db)
	total = int(total_visitor['total'])

	result.update(
			user_color = color,
			visitor_cnt_list = visitor_cnt_list,
			total_visitor = total,
			result = "success")

	return jsonify(result)

#등록된 글 수 반환
@BP.route('/posts_analysis/<int:days>')
def posts_analysis(days):
	result = {}

	posts_cnt = select_posts_cnt(g.db, days)

	result.update(
		result = "success",
		posts_cnt = posts_cnt['post_cnt'])

	return jsonify(result)

#포스트 좋아요 랭킹 반환
@BP.route('/posts_like_rank')
def posts_like_rank():
	result = {}

	like_rank = select_posts_like_rank(g.db)

	result.update(
		result = "success",
		posts_like_rank = like_rank)

	return jsonify(result)

#포스트 조회수 랭킹 반환
@BP.route('/posts_view_rank')
def posts_view_rank():
	result = {}

	view_rank = select_posts_view_rank(g.db)

	result.update(
		result = "success",
		posts_view_rank = view_rank)

	return jsonify(result)

