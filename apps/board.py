from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from global_func import *

BP = Blueprint('board', __name__)

###################################################
#페이지
@BP.route('/board/<string:pg_num>')
def page_1(pg_num):
	return render_template('board/' + pg_num + '.html')
###################################################

#게시판 반환(ex 공지사항, 자유게시판, 연애게시판 등)
@BP.route('/notice')
def get_notice():
	with g.db.cursor() as cursor:
		sql = "SELECT * FROM notice;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return jsonify(list=result, result="success")

#해당 게시판 글 목록 불러오기
@BP.route('/notice/<int:notice_id>')
def get_posts_list(notice_id):
	with g.db.cursor() as cursor:
		#포스트 정보 반환(내용 제외)
		sql = "SELECT post_id, user_id, post_title, post_view, post_date FROM post WHERE notice_id=%s;"
		cursor.execute(sql, (notice_id,))
		result_posts = cursor.fetchall()
		
		if not result_posts:
			#해당 게시판이 없을 경우
			return jsonify(result = "no have notice")
		
		#포스트 좋아요 수 결합
		for post in result_posts:
			sql = "SELECT COUNT(*) AS post_likes FROM user_like WHERE post_id=%s;"
			cursor.execute(sql, (post['post_id'],))
			result = cursor.fetchone()
			post.update(result)

		result_posts.update({"result": "success"})
	return jsonify(result_posts)

#해당 게시글 세부내용 불러오기
@BP.route('/post/<int:post_id>')
def get_post(post_id):
	with g.db.cursor() as cursor:
		#포스트 내용 반환
		sql = "SELECT * FROM post WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
		result_post = cursor.fetchone()
		
		if not result_post:
			#해당 게시글이 없을 경우
			return jsonify(resut = "no have data")

		#포스트 좋아요 수 결합
		sql = "SELECT COUNT(*) AS post_likes FROM user_like WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
		result_post_like = cursor.fetchone()
		result_post.update(result_post_like)

#select * from post join (select post_id, count(*) AS like_count from user_like group by post_id) b using(post_id);

		#포스트 댓글 결합
		sql = "SELECT comment_id, comment, user_id FROM comment WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
		result_comment = cursor.fetchall()
		result_post.update({"comment":result_comment})

		#포스트 첨부파일 경로 결합
		sql = "SELECT attachment_id, attachment_route FROM attachments WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
		result_attachment = cursor.fetchall()
		result_post.update({"attachments":result_attachment})
		result_post.update({"result": "success"})
	return jsonify(result_post)
	
