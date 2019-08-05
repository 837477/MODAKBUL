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

	scheduler.add_job(modakbul_crawler, 'cron', hour = 0, minute = 5, timezone = t_zone)
	scheduler.add_job(today_analysis, 'cron', hour = 23, minute = 58, timezone = t_zone)
	
	# weeks, days, hours, minutes, seconds
	# start_date='2010-10-10 09:30', end_date='2014-06-15 11:00'
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

#######################################################
#백그라운드 프로세스#######################################

#공모전/취업 크롤러
def modakbul_crawler():
	db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

	crawl_posts = crawl_run.crawl()
	
	#크롤러 공모전 글들
	crawl_competition = []
	#크롤러 취업 글들
	crawl_employment = []

	for post in crawl_posts:
		if '공모전' in post['tag']:
			crawl_competition.append(post)
		else:
			crawl_employment.append(post)
	
	#DB 공모전 글들
	competition_sql = select_tag_in_posts(['공모전'])
	db_competition = select_posts_list(db, competition_sql)
	#DB 취업 글들
	employment_sql = select_tag_in_posts(['취업'])
	db_employment = select_posts_list(db, employment_sql)

	#기간이 남은 공모전 글들의 타이틀만 모아놓은 리스트
	yet_competition = []

	for competition in db_competition:
		#디비에 있는 공모전 글중 기간이 지난것을 삭제.
		if competition['post_date'] < datetime.now():
			delete_post(db, competition['post_id'])
		else:
			yet_competition.append(competition['post_title'])

	#취업은 마감 기한이 없기 때문에 매번 전체 삭제 후 새롭게 크롤링 된 글로 갱신시켜준다.
	for employment in db_employment:
		delete_post(db, employment['post_id'])

	#공모전 게시글을 기존의 글과 중복검사 후 넣어준다.
	for competition in crawl_competition:
		#기존의 남아있는 공모전 글중에 안겹치는 글만 디비에 새롭게 넣어준다.(제목 비교)
		if competition['title'] not in yet_competition:
			if 'img_url' in competition:
				crawl_insert_post(db, "admin", competition['title'], competition['content'], competition['date'], competition['tag'], competition['url'], competition['img_url'])
			else:
				crawl_insert_post(db, "admin", competition['title'], competition['content'], competition['date'], competition['tag'], competition['url'], None)


	#취업 게시글은 이미 다 삭제가 되었기 때문에 새로운 크롤링 글들로 채워준다.
	for employment in crawl_employment:
		if 'img_url' in employment:
			crawl_insert_post(db, "admin", employment['title'], employment['content'], employment['date'], employment['tag'], employment['url'], employment['img_url'])
		else:
			crawl_insert_post(db, "admin", employment['title'], employment['content'], employment['date'], employment['tag'], employment['url'], None)


	db.close()

#당일 통계 관리
def today_analysis():
	db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

	#오늘 방문자 수를 가져온다.
	today_visitor_cnt = select_today_visitor_cnt(db)
	today_posts_cnt = select_today_posts_cnt(db)

	#매일 접속자 파악 테이블에 추가한다.
	result = insert_everyday_analysis(db, today_visitor_cnt['today_cnt'], today_posts_cnt['post_cnt'])

	if result:
		#정상 처리가 되었으면 하루 접속자 테이블을 리셋한다.
		reset_today_visitor(db)

