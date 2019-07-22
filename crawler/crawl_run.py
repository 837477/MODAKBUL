import iml_global
import req
from urls import urls
import warnings
from pprint import pprint
import json
#crawl_list
import wevity
import detizen
import indeed
import datetime
warnings.filterwarnings("ignore")

def crawl():
	post_list = []
	print("start")
	for idx, target in enumerate(urls):
		print("\n# " + target + " Crawling...")
		code = target.split("_")[0]
		code += ".proc('" + urls[target] + "')"
		try:
			post_list += eval(code)
		except:
			with open("crawl_error.log", "a") as f:
				f.write(str(datetime.datetime.now()) + " " + target + "\n")

	#with open("output/output.json", 'w') as outfile:
	#	json.dump(post_list, outfile)
	# title, content, date, url, tag
	return post_list

if __name__ == '__main__':
	post_list = crawl()
	for post in post_list:
		if 'img_url' in post:
			print(post['img_url'])
		else:
			print("없어!")
	