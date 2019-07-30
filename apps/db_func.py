from global_func import *
from datetime import datetime

#등록 - 반환 - 수정 - 삭제 #순서
#######################################################
#사용자 관련#############################################

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

#사용자 찾기
def select_user(db, user_id):
	with db.cursor() as cursor: 
		sql = "SELECT * FROM user WHERE user_id = %s LIMIT 1"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchone()
	return result

#사용자 태그 추가
def insert_user_tag(db, user_id, tag):
	with db.cursor() as cursor:
		sql = "INSERT INTO user_tag(user_id, tag_id) VALUES(%s, %s);"
		cursor.execute(sql, (user_id, tag,))
	db.commit()
	return "success"

#사용자 태그 반환
def select_user_tag(db, user_id):
	with db.cursor() as cursor:
		sql = "SELECT tag_id FROM user_tag WHERE user_id=%s;"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchall()

		tags = []
		for tag in result:
			tags.append(tag['tag_id'])

	return tags

#사용자 태그 삭제
def delete_user_tag(db, user_id, tag):
	with db.cursor() as cursor:
		sql = "DELETE FROM user_tag WHERE user_id=%s AND tag_id=%s;"
		cursor.execute(sql, (user_id, tag,))
	do.commit()
	return "success"

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

#사용자가 작성한 댓글들 반환
def select_user_comments(db, user_id):
	with db.cursor() as cursor:
		sql = "SELECT comment_id FROM post_comment WHERE user_id = %s;"
		cursor.execute(sql, (user_id,))

		result = cursor.fetchall()

		comments = []
		for comment in result:
			comments.append(comment['comment_id'])

	return comments

#사용자 컬러 변경
def change_user_color(db, user_id, color):
	with db.cursor() as cursor:
		sql = "UPDATE user SET user_color=%s WHERE user_id=%s;"
		cursor.execute(sql, (color, user_id,))
	db.commit()
	return "success"

#사용자 리스트 반환
def select_user_list(db):
	with db.cursor() as cursor:
		sql = "SELECT user_id, user_name, user_color FROM user;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#사용자 비밀번호 변경
def update_user_pw(db, user_id, new_pw):
	with db.cursor() as cursor:
		sql = "UPDATE user SET pw = %s WHERE user_id = %s;"
		cursor.execute(sql, (new_pw, user_id,))
	db.commit()
	return "success"

#######################################################
#보드 / 포스트 관련#######################################

#보드(메뉴) 추가 / 삭제 즉, 수정!
def update_board(db, boards):
	with db.cursor() as cursor:
		#기존 보드 삭제
		sql = "DELETE FROM baord;"
		cursor.execute(sql)

		#갱신된 보드 추가
		sql = "INSERT INTO board VALUES(%s, %s, %s, %s);"
		for board in boards:
			cursor.execute(sql, (board['board_url'], board['board_rank'], board['board_name'], board['board_access'],))
	db.commit()
	#이 방식은 랭크 수정의 편리를 위해 함 (자주 사용될 API가 아니기 때문)
	return "success"

#보드(메뉴 탭) 반환
def select_boards(db):
	with db.cursor() as cursor:
		sql = "SELECT * FROM board ORDER BY board_rank ASC;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return result 

#보드(단일) 반환
def select_board(db, board_url):
	with db.cursor() as cursor:
		sql = "SELECT * FROM board WHERE board_url = %s;"
		cursor.execute(sql, (board_url,))
		result = cursor.fetchone()
	return result

#포스트 업로드
def insert_post(db, user_id, title, content, anony, tags):
	with db.cursor() as cursor:
		sql = "INSERT INTO post (user_id, post_title, post_content, post_anony) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (user_id, title, content, anony,))
		
		sql = "SELECT MAX(post_id) AS post_id FROM post WHERE user_id = %s;"
		cursor.execute(sql, (user_id,))

		post_id = cursor.fetchone()
		post_id = post_id['post_id']

		db.commit()

		for tag in tags:
			sql = 'INSERT INTO post_tag (post_id, tag_id) VALUES (%s, %s);'
			cursor.execute(sql, (post_id, tag,))
			db.commit()

	return post_id

#해당 태그들이 속해있는 글 목록 쿼리문 반환(post_id만 반환)
def select_tag_in_posts(tag_list):	
	sql = 'SELECT P1.post_id FROM (SELECT post_id FROM post_tag WHERE tag_id = "%s") P1 '
	add_sql = 'JOIN (SELECT post_id FROM post_tag WHERE tag_id = "%s") P%s '
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
		sql = 'SELECT R.post_id AS post_id, user_id AS author_id, user_name AS author_name, user_color AS author_color, post_title, post_date, post_view, like_cnt, comment_cnt, post_anony  FROM V_post V JOIN (' + tag_in_post_id + ') R ON V.post_id = R.post_id ORDER BY V.post_date DESC LIMIT %s, %s;'
		cursor.execute(sql, ((page-1)*30, page*30))
		result = cursor.fetchall()
	return result
#태그가 속해있는 글들(ALL) 반환 (전체)
def select_posts_list(db, tag_in_post_id):
	with db.cursor() as cursor:
		sql = 'SELECT R.post_id AS post_id, user_id AS author_id, user_name AS author_name, user_color AS author_color, post_title, post_date, post_view, like_cnt, comment_cnt, post_anony  FROM V_post V JOIN (' + tag_in_post_id + ') R ON V.post_id = R.post_id ORDER BY V.post_date DESC;'
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#해당 포스트 단일 반환
def select_post(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT post_id, user_id AS author_id, post_title, post_content, post_view, post_date, post_anony, comment_cnt, like_cnt, user_id AS author_id, user_name AS author_name, user_color AS author_color FROM V_post WHERE post_id = %s;'
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

#포스트 파일 반환
def select_attach(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT file_path FROM post_attach WHERE post_id = %s;'
		cursor.execute(sql, (post_id,))
		result = cursor.fetchall()
	return result

#포스트 파일 삭제 (전체삭제)
def delete_attach(db, post_id):
	with db.cursor() as cursor:
		sql = "DELETE FROM post_attach WHERE post_id = %s;"
		cursor.execute(sql, (post_id,))
	db.commit()
	return "success"

#포스트 수정
def update_post(db, post_id, title, content, anony, user_id):
	#수정은 본인만 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user와 맞는지도 확인한다.
	with db.cursor() as cursor:
		sql = 'UPDATE post SET post_title=%s, post_content=%s, post_anony=%s WHERE post_id=%s AND user_id=%s;'
		cursor.execute(sql, (title, content, anony, post_id, user_id,))
	db.commit()
	return "success"

#포스트 삭제
def delete_post(db, post_id):
	#삭제는 ADMIN도 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user까지 비교해버리면 ADMIN 토큰으로는 삭제가 불가능 따라서 별도의 ACCESS체크 함수를 이용
	with db.cursor() as cursor:
		sql = "DELETE FROM post WHERE post_id=%s;"
		cursor.execute(sql, (post_id,))
	db.commit()
	return "success"

#포스트 부가 기능#########################################

#비밀글 확인 (0: 공개, 1:비밀 반환)
def select_private_check(db, post_id):
	with db.cursor() as cursor:
		sql = 'SELECT tag_id from post_tag WHERE post_id = %s AND tag_id="비밀글";'
		cursor.execute(sql, (post_id, ))
		result = cursor.fetchone()

		#꼼수이용! 비밀글 태그가 없으면 None을 반환하니 이것으로 판단.
		if result is None:
			return 0
		else:
			return 1

#포스트의 주인 확인 (0: 아님, 1: 맞음 반환)
def select_author_check(db, post_id, user_id):
	with db.cursor() as cursor:
		sql = "SELECT IF(user_id=%s, 1, 0) AS result FROM post WHERE post_id = %s;"
		cursor.execute(sql, (user_id, post_id,))
		result = cursor.fetchone()

	return result['result']

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
		sql = "SELECT * FROM post_like WHERE post_id=%s AND user_id=%s;"
		cursor.execute(sql, (post_id, user_id,))
		result = cursor.fetchone()

		if result is not None:
			return "already_like"

		sql = "INSERT INTO post_like (post_id, user_id) VALUES (%s, %s);"
		cursor.execute(sql, (post_id, user_id,))
	db.commit()
	return "success"

#포스트 좋아요 취소
def delete_post_like(db, post_id, user_id):
	with db.cursor() as cursor:
		sql = "DELETE FROM post_like WHERE post_id = %s AND user_id = %s;"
		cursor.execute(sql, (post_id, user_id,))
	db.commit()
	return "success"

#포스트 댓글 반환
def select_comment(db, post_id):
	with db.cursor() as cursor:
		sql = "SELECT A.comment_id, A.user_id, A.comment, A.comment_anony, A.comment_date, A.comment_parent, IF(A.comment_anony=0, B.user_name, '익명') AS author_name, IF(A.comment_anony=0, B.user_color, '#D8D8D8') AS author_color FROM post_comment A JOIN user B ON A.user_id = B.user_id WHERE post_id = %s ORDER BY A.comment_date ASC;"
		cursor.execute(sql, (post_id,))
		result = cursor.fetchall()

	return result

#포스트 댓글 쓰기 (대댓글도 동일)
def insert_comment(db, post_id, user_id, comment, anony, comment_id):
	with db.cursor() as cursor:
		sql = 'INSERT INTO post_comment (post_id, user_id, comment, comment_anony, comment_parent) VALUES (%s, %s, %s, %s, %s);'
		cursor.execute(sql, (post_id, user_id, comment, anony, comment_id,))
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

#######################################################
#투표 관련###############################################

#투표 등록 (관리자)
def insert_vote(db, vote):
	with db.cursor() as cursor:
		#투표 등록 쿼리문
		sql = 'INSERT INTO vote(user_id, vote_title, vote_content, end_date) VALUES(%s, %s, %s, %s);'
		cursor.execute(sql, (vote['user_id'], vote['title'], vote['content'], vote['end_date'],))

		#등록된 투표 아이디 가져오기.
		sql = 'SELECT MAX(vote_id) AS vote_id FROM vote WHERE user_id = %s;'
		cursor.execute(sql, (vote['user_id'],))

		vote_id = cursor.fetchone()
		vote_id = vote_id['vote_id']

		for que in vote['que_list']:
			#질문 등록 쿼리문
			sql = 'INSERT INTO vote_que(vote_id, que, que_type) VALUES(%s, %s, %s);'
			cursor.execute(sql, (vote_id, que['que'], que['que_type'],))
			
			#만약에 선택형 질문이면?
			if 'select' in que:
				#등록된 질문 아이디 가져오기.
				sql = 'SELECT MAX(que_id) AS que_id FROM vote_que;'
				cursor.execute(sql);

				que_id = cursor.fetchone()
				que_id = que_id['que_id']
				
				for select in que['select']:
					sql = 'INSERT INTO vote_select(que_id, select_content) VALUES(%s, %s);'
					cursor.execute(sql, (que_id, select,))

	db.commit()

	return vote_id

#투표 참여 (사용자)
def insert_vote_user_answer(db, user_answer):
	with db.cursor() as cursor:
		sql = 'INSERT INTO vote_user_answer(vote_id, que_id, select_id, user_id, answer) VALUES(%s, %s, %s, %s, %s);'

		#답안 리스트를 하나씩 참조
		for answer in user_answer['ans_list']:
			#만약 단답형이 아니라면?
			if answer['que_type'] != 2:
				#선택형 답안 리스트를 탐색
				for ans in answer['ans']:
					cursor.execute(sql, (user_answer['vote_id'], answer['que_id'], ans, user_answer['user_id'], None,))
			#단답형이라면?
			else:
				cursor.execute(sql, (user_answer['vote_id'], answer['que_id'], ans, user_answer['user_id'], answer['ans'],))
	db.commit()

	return "success"

#투표 글목록 반환
def select_votes(db):
	with db.cursor() as cursor:
		sql = 'SELECT A.vote_id, A.user_id AS vote_author, vote_title, vote_content, start_date, end_date, IFNULL(B.join_cnt, 0) AS join_cnt FROM vote A LEFT JOIN (SELECT vote_id, COUNT(DISTINCT user_id) AS join_cnt FROM vote_user_answer GROUP BY vote_id) B ON A.vote_id = B.vote_id WHERE A.end_date > NOW() ORDER BY A.end_date DESC;'
		cursor.execute(sql)
		result = cursor.fetchall()

	return result

#해당 투표글 반환
def select_vote(db, vote_id):
	with db.cursor() as cursor:
		sql = 'SELECT A.vote_id, A.user_id AS vote_author, vote_title, vote_content, start_date, end_date, IFNULL(B.join_cnt, 0) AS join_cnt FROM vote A LEFT JOIN (SELECT vote_id, COUNT(DISTINCT user_id) AS join_cnt FROM vote_user_answer GROUP BY vote_id) B ON A.vote_id = B.vote_id WHERE A.vote_id = %s'
		cursor.execute(sql, (vote_id,))
		result = cursor.fetchone()

	return result
#해당 투표의 질문들 반환
def select_vote_que(db, vote_id):
	with db.cursor() as cursor:
		sql = 'SELECT que_id, que, que_type FROM vote_que WHERE vote_id=%s;'
		cursor.execute(sql, (vote_id,))
		result = cursor.fetchall()

	return result
#해당 질문의 선택지들 반환
def select_vote_select(db, que_id):
	with db.cursor() as cursor:
		sql = 'SELECT select_id, select_content FROM vote_select WHERE que_id=%s;'
		cursor.execute(sql, (que_id,))
		result = cursor.fetchall()

	return result

#투표 파일 등록
def insert_vote_attach(db, vote_id, file):
	with db.cursor() as cursor:
		sql = "INSERT INTO vote_attach (vote_id, vote_file_path) VALUES (%s, %s);"
		cursor.execute(sql, (vote_id, file,))
	db.commit()
	return "success"

#투표 파일 반환
def select_vote_attach(db, vote_id):
	with db.cursor() as cursor:
		sql = 'SELECT vote_file_path FROM vote_attach WHERE vote_id = %s;'
		cursor.execute(sql, (vote_id,))
		result = cursor.fetchall()
	return result

#투표 수정 (마감 기한만 가능)
def update_vote(db, user_id, end_date):
	#수정은 본인만 가능해야 하므로 AND 연산으로 해당 토큰으로 받은 user와 맞는지도 확인한다
	with db.cursor() as cursor:
		sql = 'UPDATE vote SET end_date=%s WHERE vote_id=%s; AND user_id=%s;'
		cursor.execute(sql, (end_date, user_id,))
	db.commit()
	return "success"

#투표 삭제
def delete_vote(db, vote_id, user_id):
	#투표 삭제는 어드민만 가능! (어차피 작성자 또한 어드민)
	with db.cursor() as cursor:
		sql = "DELETE FROM vote WHERE vote_id=%s AND user_id=%s;"
		cursor.execute(sql, (vote_id, user_id))
	db.commit()
	return "success"

#중복 투표 체크
def check_already_vote(db, vote_id, user_id):
	with db.cursor() as cursor:
		sql = 'SELECT EXISTS (SELECT * FROM vote_user_answer WHERE vote_id=%s AND user_id=%s) AS success;'
		cursor.execute(sql, (vote_id, user_id,))
		result = cursor.fetchone()
	return result['success']

#######################################################
#접근 권환 확인 ##########################################

#포스트 삭제 권한 확인
def access_check_post(db, post_id, user_id):
	#관리자 체크
	if check_admin(db, user_id):
		return 1

	with db.cursor() as cursor:
		sql = 'SELECT IF(user_id = %s, 1, 0) AS access FROM post WHERE post_id = %s;'
		cursor.execute(sql, (user_id, post_id,))
		result = cursor.fetchone()
	return result['access']

#댓글 삭제 권환 확인
def access_check_comment(db, comment_id, user_id):
	#관리자 체크
	if check_admin(db, user_id):
		return 1

	with db.cursor() as cursor:
		sql = 'SELECT IF(user_id = %s, 1, 0) AS access from post_comment where comment_id = %s;'
		cursor.execute(sql, (user_id, comment_id, ))
		result = cursor.fetchone()
	return result['access']

#관리자 확인
def check_admin(db, user_id):
	if "ADMIN" in select_user_tag(db, user_id):
		return True
	else:
		return False

#######################################################
#검색 엔진###############################################

#작성자 / 제목 / 타이틀 검색!
def select_search(db, topic_list):
	with db.cursor() as cursor:
		sql = 'SELECT * FROM v_post WHERE '

		for topic in topic_list:
			#작성자 찾기
			sql += 'user_name LIKE '
			like_topic = '"%' + topic + '%" OR '
			sql += like_topic

			#타이틀 찾기
			sql += 'post_title LIKE '
			like_topic = '"%' + topic + '%" OR '
			sql += like_topic

			#본문 찾기
			sql += 'post_content LIKE '
			like_topic = '"%' + topic + '%"'
			sql += like_topic

			if topic is not topic_list[-1]:
				sql += ' OR '

		sql += ' ORDER BY post_date DESC;'
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#######################################################
#관리자 전용#############################################

#정적 variable 추가
def insert_variable(db, key, value):
	with db.cursor() as cursor:
		sql = "INSERT INTO variable VALUES(%s, %s);"
		cursor.execute(sql, (key, value,))
	db.commit()

	return "success"

#정적 variable 리스트 반환
def select_variables(db):
	with db.cursor() as cursor:
		sql = 'SELECT * FROM variable;'
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#정적 varialbe의 특정 value 반환
def select_value(db, key):
	with db.cursor() as cursor:
		sql = "SELECT value FROM variable WHERE v_key=%s;"
		cursor.execute(sql, (key,))
		result = cursor.fetchone()
	return result

#정적 variable 삭제
def delete_variable(db, key):
	with db.cursor() as cursor:
		sql = 'DELETE FROM variable WHERE v_key=%s;'
		cursor.execute(sql, (key,))
	db.commit()

	return "success"

#부서 등록
def insert_department(db, dm_name, dm_chairman, dm_intro):
	with db.cursor() as cursor:
		sql = "INSERT INTO department(dm_name, dm_chairman, dm_intro) VALUES(%s, %s, %s);"
		cursor.execute(sql, (dm_name, dm_chairman, dm_intro,))
	db.commit()

	return "success"

#부서 반환
def select_department(db):
	with db.cursor() as cursor:
		sql = "SELECT * FROM department;"
		cursor.execute(sql)
		result = cursor.fetchall()
	return result

#부서 삭제
def delete_department(db, dm_id):
	with db.cursor() as cursor:
		sql = 'DELETE FROM department WHERE dm_id=%s;'
		cursor.execute(sql, (dm_id,))
	db.commit()

	return "success"

#######################################################
#로그 기록###############################################

#로그 등록
def insert_log(db, user_id, log_url):
	with db.cursor() as cursor:
		sql = 'INSERT INTO log(user_id, log_url) VALUES(%s, %s);'
		cursor.execute(sql, (user_id, log_url,))
	db.commit()
	return "success"

#######################################################
#로그 기록###############################################



