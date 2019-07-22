import requests
from bs4 import BeautifulSoup as bs

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
			AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
			"Accept":"text/html,application/xhtml+xml,application/xml;\
			q=0.9,imgwebp,*/*;q=0.8"}

def get_soup(url):
	with requests.Session() as s:
		html = s.get(url, headers=header, verify = False).text
	obj = bs(html, "html.parser")
	return obj