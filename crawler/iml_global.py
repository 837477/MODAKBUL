import sys
import datetime
sys.path.insert(0,'./')
sys.path.insert(0,'./crawlers')

def today():
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")
	return date
def mday(day):
	now = datetime.datetime.now() - datetime.timedelta(days = day)
	date = now.strftime("%Y-%m-%d %H:%M:%S")

	return date
def date_format(date_str):
	date_str = date_str.replace(".","-")
	if len(date_str) == 10:
		return date_str + " 23:59:59"

def main_domain(url):
	url_ = url.split("/")
	result = url_[0] + "//"
	result += url_[2] + "/"
	return result

def domain(url):
	url_ = url.split("/")
	result = url_[0] + "//"
	for i in url_[2:-1]:
		result += i + "/"
	return result