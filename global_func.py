import sys
sys.path.insert(0,'./')
sys.path.insert(0,'./database')
sys.path.insert(0,'./apps')
sys.path.insert(0,'./crawler')
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
from init_database import *
from db_func import *
import crawl_run

# BackgroundScheduler Initialize
def schedule_init():
	t_zone = get_localzone()
	scheduler = BackgroundScheduler()
	#scheduler.add_job(func = test_bg, trigger = "interval", seconds = 1, timezone = t_zone)
	scheduler.add_job(modakbul_crawler, 'cron', hour = 0, minute = 30, timezone = t_zone)
	scheduler.add_job(today_analysis, 'cron', hour = 23, minute = 59, timezone = t_zone)
	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

#######################################################
#백그라운드 프로세스#######################################

#공모전/취업 크롤러
def modakbul_crawler():
	db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

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

#당일 통계 관리
def today_analysis():
	db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

	#오늘 방문자 수를 가져온다.
	today_visitor_cnt = select_today_visitor_cnt(g.db)
	today_posts_cnt = select_today_posts_cnt(g.db)

	#매일 접속자 파악 테이블에 추가한다.
	result = insert_everyday_analysis(g.db, today_visitor_cnt['today_cnt'], today_posts_cnt['post_id'])

	if result:
		#정상 처리가 되었으면 하루 접속자 테이블을 리셋한다.
		reset_today_visitor(g.db)

