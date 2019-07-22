import req
from iml_global import *
def proc(url):
	index = 1
	result = []
	while(True):
		print("## " + str(index) + " Page")
		temp, quit = get_posts(url + str(index))
		result += temp
		if quit: break
		index += 1
	return result

def get_posts(url):
	result = []	
	soup = req.get_soup(url)
	soup = soup.select("ul.list > li")[1:]
	for tag in soup:
		post_url = domain(url) + tag.a.attrs['href']
		temp = get_post(post_url)
		if temp is None: return result, True
		print(temp['title'], temp['date'])
		result += [temp]
	return result, False

def get_post(url):
	soup = req.get_soup(url)
	title = soup.select("h6.tit")[0].get_text()
	date = soup.select("li.dday-area")[0].get_text()
	date = date_format(date.split("~ ")[1][:10])
	content = soup.select("div#viewContents")[0].get_text()
	if today() > date: return None
	return {"title":title.strip(),
			"date":date.strip(),
			"content":content.strip(),
			"url":url,
			"tag":["공모전","외부사이트"]}