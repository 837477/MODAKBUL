import sys
sys.path.insert(0,'./')
sys.path.insert(0,'./database')
sys.path.insert(0,'./apps')
sys.path.insert(0,'./crawler')
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone
from init_database import *

import crawler_main

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
	crawl_posts = crawler_main.crawl()
	print(crawl_posts)