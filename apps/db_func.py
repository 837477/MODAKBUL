from global_func import *
#사용자 관련############################################

#사용자 찾기
def select_user(db, user_id):
	with db.cursor() as cursor: 
		sql = "SELECT * FROM user WHERE user_id = %s LIMIT 1"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchone()
	return result

#사용자 추가
def insert_user(db, user_data, user_major):
	with db.cursor() as cursor:
		#user 테이블에 회원정보 추가
		sql = "INSERT INTO user(user_id, pw, user_name) VALUES (%s, %s, %s);"
		cursor.execute(sql, user_data)
		#user_tag 테이블에 학과태그 추가
		sql = "INSERT INTO user_tag(user_id, tag_id) VALUES (%s, %s);"
		cursor.execute(sql, (user_data[0], user_major))
	db.commit()
	return "success"

#사용자가 태그 반환
def select_user_tag(db, user_id):
	with db.cursor() as cursor:
		sql = "SELECT tag_id FROM user_tag WHERE user_id=%s;"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchall()

		tags = []
		for tag in result:
			tags.append(tag['tag_id'])

	return tags

#사용자가 좋아요 한 게시물 반환
def select_user_post_like(db, user_id):
	with db.cursor() as cursor:
		sql = "SELECT post_id FROM post_like WHERE user_id=%s;"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchall()

		like_posts = []
		for post in result:
			like_posts.append(post['post_id'])

	return like_posts

#사용자 컬러 변경
def change_user_color(db, user_id, color):
	with db.cursor() as cursor:
		sql = "UPDATE user SET user_color=%s WHERE user_id=%s;"
		cursor.execute(sql, (color, user_id,))
	db.commit()

#보드 관련#############################################

#보드 테이블 반환
def select_board(db):
	with db.cursor() as cursor:
		sql = "SELECT board_name, board_url AS board_tag FROM board;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return result 

#태그가 속해있는 글의 아이디(post_id)들을 반환 (쿼리문형식, 중복가능)
def select_tag_in_posts(tag_list):	
	sql = 'SELECT P1.post_id FROM (SELECT post_id FROM post_tag WHERE tag_id LIKE "%s") P1 '
	add_sql = 'JOIN (SELECT post_id FROM post_tag WHERE tag_id LIKE "%s") P%s '
	i = 2
	result_sql = ""

	for tag in tag_list:
		if tag == tag_list[0]:
			result_sql +=(sql %(tag))

		elif tag != tag_list[len(tag_list)-1]:
			result_sql +=(add_sql %(tag, i))
			i +=1
			
		else:
			result_sql +=(add_sql %(tag, i))
			i +=1
			result_sql += "ON P1.post_id = P2.post_id "
			for i in range(3, i):
				temp = "AND P1.post_id = P%s.post_id "
				temp = (temp %(i))
				result_sql += temp
			#result_sql += ';'
	return result_sql

#태그가 속해있는 글들(ALL) 반환 (페이지네이션)
def select_posts_page(db, tag_in_post_id, page):
	with db.cursor() as cursor:
		sql = 'SELECT R.post_id AS post_id, user_id AS post_author, user_name AS author_name, post_title, post_date, post_view, like_cnt, comment_cnt, post_anony  FROM V_post V JOIN (' + tag_in_post_id + ') R ON V.post_id = R.post_id LIMIT %s, %s;'
		cursor.execute(sql, ((page-1)*30, page*30))
		result = cursor.fetchall()
	return result
#태그가 속해있는 글들(ALL) 반환 (전체)
def select_posts_list(db, tag_in_post_id):
	with db.cursor() as cursor:
		sql = 'SELECT R.post_id AS post_id, user_id AS post_author, user_name AS author_name, post_title, post_date, post_view, like_cnt, comment_cnt, post_anony  FROM V_post V JOIN (' + tag_in_post_id + ') R ON V.post_id = R.post_id;'
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#해당 포스트 단일 반환
def select_post(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT * FROM V_post WHERE post_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchone()
	return result

#포스트 미리보기 글들 반환 (갤러리 전용, 페이지네이션)
def select_gallery_posts(db, tag_in_post_id, page):
	with db.cursor() as cursor:
		sql = 'SELECT post.post_id, post_title FROM post JOIN (' + tag_in_post_id + ') R ON post.post_id = r.post_id LIMIT %s, %s;'
		cursor.execute(sql, ((page-1)*30, page*30))
		result = cursor.fetchall()
	return result

#포스트 파일 반환
def select_attach(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT file_path FROM post_attach WHERE post_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchall()
	return result

#업로드 / 수정 / 권한체크 #################################

#포스트 업로드
def insert_post(db, user_id, title, content, anony, tags):
	with db.cursor() as cursor:
		sql = "INSERT INTO post (user_id, post_title, post_content, post_anony) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (user_id, title, content, anony,))
		
		sql = "SELECT MAX(post_id) AS post_id FROM post"
		cursor.execute(sql)

		post_id = cursor.fetchone()

		db.commit()

		for tag in tags:
			sql = 'INSERT INTO post_tag (post_id, tag_id) VALUES (%s, %s);'
			cursor.execute(sql, (post_id['post_id'], tag,))
			db.commit()

	return post_id['post_id']

#포스트 수정
def update_post(db, post_id, title, content, anony, user_id):
	#수정은 본인만 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user와 맞는지도 확인한다.
	with db.cursor() as cursor:
		sql = 'UPDATE post SET post_title="%s", post_content="%s", post_anony=%s WHERE post_id=%s; AND user_id=%s;'
		cursor.execute(sql, (title, content, anony, post_id, user_id,))
	db.commit()
	return "success"

#포스트 삭제
def delete_post(db, post_id):
	#삭제는 ADMIN도 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user까지 비교해버리면 ADMIN 토큰으로는 삭제가 불가능 따라서 별도의 ACCESS체크 함수를 이용
	with db.cursor() as cursor:
		sql = "DELETE FROM post WHERE post_id=%s;"
		cursor.execute(sql, (post_id, user_id))
	db.commit()
	return "success"

#포스트 파일 업로드
def insert_attach(db, post_id, file, file_S):
	with db.cursor() as cursor:
		sql = "INSERT INTO post_attach (post_id, file_path) VALUES (%s, %s);"
		cursor.execute(sql, (post_id, file,))

		if file_S is not None:
			sql = "INSERT INTO post_attach (post_id, file_path) VALUES (%s, %s);"
			cursor.execute(sql, (post_id, file_S,))
	db.commit()
	return "success"

#포스트 파일 삭제 (단일 삭제가 아님. 전체삭제)
def delete_attach(db, post_id):
	with db.cursor() as cursor:
		sql = "DELETE FROM post WHERE post_id = %s"
		cursor.execute(sql, (post_id,))
	db.commit()
	return "success"

#조회수 / 댓글 / 좋아요 ##################################

#포스트 조회수 증가
def update_view(db, post_id):
	with db.cursor() as cursor:
		sql = "UPDATE post SET post_view = post_view + 1 WHERE post_id = %s;"
		cursor.execute(sql, (post_id,))
	db.commit()
	return "success"

#포스트 좋아요 등록
def insert_post_like(db, post_id, user_id):
	with db.cursor() as cursor:
		sql = "INSERT INTO post_like (post_id, user_id) VALUES (%s, %s);"
		cursor.execute(sql, (post_id, user_id,))
	db.commit()
	return "success"

#포스트 좋아요 취소
def delete_post_like(db, post_id, user_id):
	with db.cursor() as cursor:
		sql = "DELETE FROM post_like WHERE post_id = %s AND user_id = %s"
		cursor.execute(sql, (post_id, user_id,))
	db.commit()
	return "success"

#포스트 댓글 반환
def select_comment(db, post_id):
	with db.cursor() as cursor:
		sql = "SELECT A.comment_id, A.user_id, A.comment, A.comment_anony, A.comment_date, A.comment_parent, B.user_name  FROM post_comment A JOIN user B ON A.user_id = B.user_id WHERE post_id = %s;"
		cursor.execute(sql, (post_id,))
		result = cursor.fetchall()
	return result

#포스트 댓글 쓰기
def insert_comment(db, post_id, user_id, comment, anony):
	with db.cursor() as cursor:
		sql = "INSERT INTO post_comment (post_id, user_id, comment, anony) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (post_id, user_id, comment, anony,))
	db.commit()
	return "success"

#포스트 댓글 수정
def update_comment(db, comment_id, comment, anony, user_id):
	with db.cursor() as cursor:
		sql = 'UPDATE post_comment SET comment = "%s", comment_anony = "%s" WHERE comment_id = %s AND user_id = %s;'
		cursor.execute(sql, (comment, anony, user_id,))
	db.commit()
	return "success"

#포스트 댓글 삭제
def delete_comment(db, comment_id):
	#삭제는 ADMIN도 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user까지 비교해버리면 ADMIN 토큰으로는 삭제가 불가능 따라서 별도의 ACCESS체크 함수를 이용
	with db.cursor() as cursor:
		sql = 'DELETE FROM post_comment WHERE comment_id=%s;'
		cursor.execute(sql, (comment_id,))
	db.commit()
	return "success"

#접근 권환 확인 ####################################
#수정권한은 쿼리문에서 AND로 비교한다.
#포스트 삭제 권한 확인
def access_check_post(db, post_id, user_id):
	if user_id is "ADMIN":
		return 1

	with db.cursor() as cursor:
		sql = 'SELECT IF(user_id = "%s", 1, 0) AS access from post where post_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchone()
	return result['access']

#댓글 삭제 권환 확인
def access_check_comment(db, comment_id, user_id):
	if user_id is "ADMIN":
		return 1

	with db.cursor() as cursor:
		sql = 'SELECT IF(user_id = "%s", 1, 0) AS access from post_comment where comment_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchone()
	return result['access']

#
