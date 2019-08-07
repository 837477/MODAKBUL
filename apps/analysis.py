from flask import *
from werkzeug import *
from flask_jwt_extended import *
from db_func import *
from word_filter import *

BP = Blueprint('analysis', __name__)
#######################################################
#페이지 URL#############################################
@BP.route('/statistics')
def statistics():
	today = select_today_visitor(g.db)

	if request.remote_addr not in today:
		#방문자 기록
		insert_today_visitor(g.db, request.remote_addr)

	return render_template('analysis/statistics.html')
#######################################################
#통계 관련3##############################################

#누적 통계 반환 (OK)
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

	#기간 내 통 목록 반환
	everyday_analysis = select_everyday_analysis(g.db, days)

	#오늘 방문자 수 반환
	today_visitor = select_today_visitor_cnt(g.db)
	today = today_visitor['today_cnt']

	#전체 방문자 수 반환
	total_visitor = select_everyday_visitor_total(g.db)
	total = total_visitor['total']
	total = int(total) + today

	result.update(
			user_color = color,
			everyday_analysis = everyday_analysis,
			today_visitor = today,
			total_visitor = total,
			result = "success")

	return jsonify(result)

#포스트 좋아요 랭킹 반환 (OK)
@BP.route('/posts_like_rank/<int:days>')
def posts_like_rank(days):
	result = {}

	like_rank = select_posts_like_rank(g.db, days)

	result.update(
		result = "success",
		posts_like_rank = like_rank)

	return jsonify(result)

#포스트 조회수 랭킹 반환 (OK)
@BP.route('/posts_view_rank/<int:days>')
def posts_view_rank(days):
	result = {}

	view_rank = select_posts_view_rank(g.db, days)

	result.update(
		result = "success",
		posts_view_rank = view_rank)

	return jsonify(result)

#투표 현황(진행중 / 완료) 반환 (OK)
@BP.route('/get_vote_status')
def get_vote_status():
	result = {}

	undone_vote = select_votes(g.db)
	done_vote = select_votes_finish(g.db)

	for vote in undone_vote:
		#프론트의 요구로 날짜 형식 변형
		vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
		vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	for vote in done_vote:
		#프론트의 요구로 날짜 형식 변형
		vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
		vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	result.update(
		result = "success",
		undone_vote = undone_vote,
		done_vote = done_vote)
 
	return jsonify(result)

#해당 투표의 선택지 점유율 (OK)
@BP.route('/get_vote_select_status/<int:vote_id>')
def get_vote_select_status(vote_id):
	result = {}
	vote = select_vote(g.db, vote_id)

	if vote is None:
		return jsonify(reuslt = "define vote")

	ques = select_vote_que(g.db, vote_id)

	#프론트의 요구로 날짜 형식 변형
	vote['start_date'] = vote['start_date'].strftime("%Y년 %m월 %d일")
	vote['end_date'] = vote['end_date'].strftime("%Y년 %m월 %d일")

	for que in ques:
		select = select_vote_select_status(g.db, que['que_id'])
		que.update(select = select)

	vote.update(que_list = ques)

	result.update(
		vote = vote,
		result = "success")

	return jsonify(result)

#해당 질문의 선택지 현황 (선택한 유저목록 및 단답형 대답 반환) (OK)
@BP.route('/get_vote_select_status_user/<int:que_id>')
@jwt_required
def get_vote_select_status_user(que_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		return jsonify(result = "you are not admin")

	result = {}

	select_user_list = select_vote_select_status_user(g.db, que_id)

	result.update(
		result = "success",
		select_user_list = select_user_list)

	return jsonify(result)
	

	

	

