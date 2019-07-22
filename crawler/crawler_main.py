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
warnings.filterwarnings("ignore")

def crawl():
	post_list = []
	print("start")
	for idx, target in enumerate(urls):
		print("\n# " + target + " Crawling...")
		code = target.split("_")[0]
		code += ".proc('" + urls[target] + "')"
		post_list += eval(code)
	#with open("output/output.json", 'w') as outfile:
	#	json.dump(post_list, outfile)
	# title, content, date, url, tag, emg_url
	return post_list

if __name__ == '__main__':
	pass#main()
	