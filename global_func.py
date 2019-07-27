import sys
sys.path.insert(0,'./')
sys.path.insert(0,'./database')
sys.path.insert(0,'./apps')
sys.path.insert(0,'./crawler')
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
from init_database import *

import crawl_run

# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()
	#scheduler.add_job(func = test_bg, trigger = "interval", seconds = 1, timezone = t_zone)
	scheduler.add_job(func = modakbul_crawler, trigger = "interval", days = 1, timezone = t_zone)
	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

########## 백그라운드 프로세스 ##########
def modakbul_crawler():
	db = db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

	#기존 공모전/취업글 삭제
	c_delete_post(db)

	#새롭게 크롤링 시작
	crawl_posts = crawl_run.crawl()
	
	#새로운 글들 디비 저장.
	if crawl_posts is not None:
		for crawl_post in crawl_posts:
			if 'img_url' in crawl_post:
				c_insert_post(db, "ADMIN", crawl_post['title'], crawl_post['content'], crawl_post['date'], crawl_post['tag'], crawl_post['url'], crawl_post['img_url'])
			else:
				c_insert_post(db, "ADMIN", crawl_post['title'], crawl_post['content'], crawl_post['date'], crawl_post['tag'], crawl_post['url'], "NULL")
	
	db.close()

#DB 이용 함수###########################################
#크롤러 사이트 포스트들 업로드 전용 함수
def c_insert_post(db, user_id, title, content, date, tags, url, img_url):
	with db.cursor() as cursor:
		sql = "INSERT INTO post (user_id, post_title, post_content, post_date) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (user_id, title, content, date,))
		
		sql = "SELECT MAX(post_id) AS post_id FROM post"
		cursor.execute(sql)

		post_id = cursor.fetchone()

		tags.append('대외활동')

		for tag in tags:
			sql = 'INSERT INTO post_tag (post_id, tag_id) VALUES (%s, %s);'
			cursor.execute(sql, (post_id['post_id'], tag,))

		sql = "INSERT INTO post_url (post_id, post_url_link, post_url_img) VALUES (%s, %s, %s);"

		cursor.execute(sql, (post_id['post_id'], url, img_url,))

	db.commit()

#크롤러 사이트 포스트들 전체 삭제 전용 함수
def c_delete_post(db):
	target_posts = c_select_tag_in_posts(db, ['외부사이트'])
	
	with db.cursor() as cursor:
		sql = 'DELETE FROM post WHERE post_id = %s;'
		
		for post in target_posts:
			cursor.execute(sql, (post['post_id'],))

		db.commit()

	return "success"

#외부사이트 태그가 들어가있는 포스트 아이디들 반환해주는 함수
def c_select_tag_in_posts(db, tag_list):	
	with db.cursor() as cursor:
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
				result_sql += ';'
		
		cursor.execute(result_sql)
		result = cursor.fetchall()

	return result