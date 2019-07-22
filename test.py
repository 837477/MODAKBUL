import requests
import json
from pprint import pprint
#shin10256
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjM0Njc0NTgsIm5iZiI6MTU2MzQ2NzQ1OCwianRpIjoiODA5ZmMzY2QtMTU3Mi00NWYxLWFjN2ItYzU0NTQ4NjU1Y2I2IiwiaWRlbnRpdHkiOiIxNjAxMTA3NSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.uyoGJRhz5Ggj1bWh7xlLgyW4gSOCCrErOwHVF4mEzvQ"

header = {
	'Authorization':"Bearer " + token
}
#Debug Here
url = "http://localhost:5000/posts/공모전_소프트웨어융합대학"
data = {

}
######
html = requests.get(url, headers =header, data = data).content
#html = requests.post(url, headers =header, data = data).content
pprint(html)