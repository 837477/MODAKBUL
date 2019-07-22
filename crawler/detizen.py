import req
from iml_global import *
def proc(url):
	index = 1
	result = []
	while(True):
		print("## " + str(index) + " Page")
		temp = get_posts(url + str(index))
		if not temp: break
		result += temp
		index += 1
	return result

def get_posts(url):
	result = []	
	soup = req.get_soup(url)
	soup = soup.findAll("div", {"class":"main-info clearfix"})
	for tag in soup:
		tag_ = tag.select("h4 > a")[0]
		post_url = domain(url) + tag_.attrs['href']
		temp = get_post(post_url)
		if not temp: continue
		print(temp['title'], temp['date'])
		result += [temp]

	return result

def get_post(url):
	soup = req.get_soup(url)
	title = soup.select("span.on")[0].get_text()
	date = soup.find("th", text = "기간").parent.select("td")[0].get_text()
	date = date_format(date.split("~ ")[1][:10])
	img_url = main_domain(url) + soup.select("div.poster > img")[0].attrs['src'][1:]
	content = soup.select("ul.summary-info")[0].get_text()
	if today() > date: return None
	return {"title":title.strip(),
			"date":date.strip(),
			"content":content.strip(),
			'url':url,
			"img_url":img_url,
			"tag":["공모전","외부사이트"]}