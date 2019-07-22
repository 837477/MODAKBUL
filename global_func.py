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
	print("asd")
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()
	#scheduler.add_job(func = test_bg, trigger = "interval", seconds = 1, timezone = t_zone)
	scheduler.add_job(func = test_bg, trigger = "interval", hours = 1, timezone = t_zone)
	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

########## 백그라운드 프로세스 ##########
def modakbul_crawler():
	crawl_posts = crawler_runß.crawl()
	
	for crawl_post in crawl_posts:
		if 'img_url' in crawl_post:
			g_insert_post(g.db, "ADMIN", crawl_post['title'], crawl_post['content'], crawl_post['date'], crawl_post['tag'], crawl_post['url'], crawl_post['img_url'])
		else:
			g_insert_post(g.db, "ADMIN", crawl_post['title'], crawl_post['content'], crawl_post['date'], crawl_post['tag'], crawl_post['url'], None)

#DB 이용 함수#########################
#크롤러 사이트 포스트들 업로드 전용 함수
def g_insert_post(db, user_id, title, content, date, tags, url, img_url):
	with db.cursor() as cursor:
		sql = "INSERT INTO post (user_id, post_title, post_content, post_date) VALUES (%s, %s, %s, %s);"
		cursor.execute(sql, (user_id, title, content, anony,))
		
		sql = "SELECT MAX(post_id) AS post_id FROM post"
		cursor.execute(sql)

		post_id = cursor.fetchone()

		db.commit()

		for tag in tags:
			sql = 'INSERT INTO post_tag (post_id, tag_id) VALUES (%s, %s);'
			cursor.execute(sql, (post_id['post_id'], tag,))
			db.commit()

		###########post_url에 url추가 작업 이어서 하면 됨.

	return post_id['post_id']

#{'title': 'IT Specialist', 'date': '2019-07-23 00:37:26', 'content': '인디드 취업 정보', 'url': 'https://kr.indeed.com//rc/clk?jk=85ca1babdd5c7a9c&fccid=bca1c8ed48c3b338&vjs=3', 'tag': ['취업', '외부사이트']}

#img_url도 있음!