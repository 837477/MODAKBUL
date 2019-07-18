from global_func import *
from sejong_account import sejong_api

#사용자 관련###################################################

#사용자 찾기
def select_user_id(db, user_id):
	with db.cursor() as cursor: 
		sql = "SELECT * FROM user WHERE user_id = %s LIMIT 1"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchone()
		return result

#사용자 학과 반환
def select_user_major(db, user_id):
	with db.cursor() as cursor:
		sql = "SELECT tag_id FROM user_tag WHERE user_id=%s;"
		cursor.execute(sql, (user_id,))
		result = cursor.fetchone()
		return result['tag_id']

#사용자 컬러 변경
def change_user_color(db, user_id, color):
	with db.cursor() as cursor:
		sql = "UPDATE user SET user_color=%s WHERE user_id=%s;"
		cursor.execute(sql, (color, user_id,))
	g.db.commit()

############################################################