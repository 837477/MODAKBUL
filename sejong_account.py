import requests
from bs4 import BeautifulSoup as bs
import getpass

# API 확실하게 하자 -> do.sejong.ac.kr의 확실한 방식 탐색
def sejong_api(id, pw):
	data = {"username":id, "password":pw, "rememberusername":"1"}
	with requests.Session() as s:
		page = s.post("http://sjulms.moodler.kr/login/index.php", data = data)
		soup = bs(page.text, "html.parser")
		if soup.find("h4") is None:
			return {"result":False}
		else:
			name = soup.find("h4").get_text()
			major = soup.find("p",{"class":"department"}).get_text()
			return {
			"result":True,
			"name":name,
			"major":major
			}
