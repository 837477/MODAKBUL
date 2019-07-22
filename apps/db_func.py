from global_func import *
#IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
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

#업로드 / 수정###############################################

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
def update_post(db, post_id, title, content, anony):
	with db.cursor() as cursor:
		sql = 'UPDATE post SET post_title="%s", post_content="%s", post_anony=%s WHERE post_id=%s;'
		cursor.execute(sql, (title, content, anony, post_id,))
	db.commit()
	return "success"

#포스트 삭제
def delete_post(db, post_id):
	with db.cursor() as cursor:
		sql = "DELETE FROM post WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
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

