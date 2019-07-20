from global_func import *
from sejong_account import sejong_api
IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
#사용자 관련############################################

#사용자 찾기
def select_user_id(db, user_id):
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

		tages = []
		for tag in result:
			tages.append(tag['tag_id'])

	return tages

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
		sql = "SELECT * FROM board;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return result 

#태그가 속해있는 글 아이디(post_id)들 반환해주는 스트링(쿼리문) 반환 (중복 가능)
def select_posts_in_tag(tag_list):	
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
def select_posts_page(db, post_in_tag_SQL, page):
	with db.cursor() as cursor:
		sql = 'SELECT * from V_post V JOIN (' + post_in_tag_SQL + ') R ON V.post_id = R.post_id LIMIT %s, %s;'
		cursor.execute(sql, ((page-1)*30, page*30))
		result = cursor.fetchall()
	return result
#태그가 속해있는 글들(ALL) 반환 (전체)
def select_posts_list(db, post_in_tag_SQL):
	with db.cursor() as cursor:
		sql = 'SELECT * from V_post V JOIN (' + post_in_tag_SQL + ') R ON V.post_id = R.post_id;'
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#해당 포스트들의 파일들 반환
def select_files(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT file_path FROM post_attach WHERE post_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchall()
	return result

#포스트 글들 반환 (갤러리 전용, 페이지네이션)
def select_gallery_post(db, post_in_tag_SQL, page):
	with db.cursor() as cursor:
		sql = 'SELECT post.post_id, post_title FROM post JOIN (' + post_in_tag_SQL + ') R ON post.post_id = r.post_id LIMIT %s, %s;'
		cursor.execute(sql, ((page-1)*30, page*30))
		result = cursor.fetchall()

		for post in result:
			db_files = select_files(db, post['post_id'])

			files = []

			for file in db_files:
				if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] == "S_":
					files.append(file['file_path'])

			post.update(files = files)
	return result

#업로드 ###############################################

#파일 업로드
def insert_attach(db, post_id, file, file_S):
	with db.cursor() as cursor:
		sql = "INSERT INTO post_attach (post_id, file_path) VALUES (%s, %s);"
		cursor.execute(sql, (post_id, file,))

		if file_S is not None:
			sql = "INSERT INTO post_attach (post_id, file_path) VALUES (%s, %s);"
			cursor.execute(sql, (post_id, file_S,))
	db.commit()
	return "success"

#포스트 업로드
def insert_post(db, user_id, title, content, anony, tages):
	with db.cursor() as cursor:
		sql = "INSERT INTO post (user_id, post_title, post_content, post_anony) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (user_id, title, content, anony,))
		
		sql = "SELECT MAX(post_id) AS post_id FROM post"
		cursor.execute(sql)

		post_id = cursor.fetchone()

		db.commit()

		for tag in tages:
			sql = 'INSERT INTO post_tag (post_id, tag_id) VALUES (%s, %s);'
			cursor.execute(sql, (post_id['post_id'], tag))
			db.commit()

	return post_id['post_id']

