from flask import *
from werkzeug.security import *
from flask_jwt_extended import *
from db_func import *

BP = Blueprint('board', __name__)

###################################################
#페이지
@BP.route('/board/<string:pg_num>')
def page_1(pg_num):
	return render_template('board/' + pg_num + '.html')
###################################################

#게시판 반환(ex 공지사항, 학생회비 사용내역 등)
@BP.route('/board')
def get_board():
	board = select_board(g.db)
	return jsonify(board)

#게시판 글 목록 불러오기
#@BP.route('/post/<string:tag_string>')
#def get_posts_list(tag_string):
	

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
	
