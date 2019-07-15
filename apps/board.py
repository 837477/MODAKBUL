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
@BP.route('/get-notice')
def get_notice():
	with g.db.cursor() as cursor:
		sql = "SELECT * FROM notice;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return jsonify(list=result, result="success")

#해당 게시판의 게시물 전체 반환
@BP.route('/get-post/<int:notice_id>')
def get_post(notice_id):
	with g.db.cursor() as cursor:
		#포스트 순수 내용 반환
		sql = "SELECT * FROM post WHERE notice_id=%s;"
		cursor.execute(sql, (notice_id,))
		result_post = cursor.fetchall()
		
		#첨부파일 반환 후 result_post에 추가
		sql_attachments = "SELECT attachment_id, attachment_route FROM attachments WHERE post_id=%s;"
		sql_likes = "SELECT COUNT(*) FROM user_like WHERE post_id=%s;"

		for temp in result_post:
			cursor.execute(sql_attachments, (temp['post_id'],))
			attachment_result = cursor.fetchall()
			temp.update({"attachments":attachment_result})

		
		#해당 게시글의 좋아요 갯수 반환
		


	return jsonify(result_post)


