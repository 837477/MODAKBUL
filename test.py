import requests
import json
from pprint import pprint
#shin10256
#token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjM0Njc0NTgsIm5iZiI6MTU2MzQ2NzQ1OCwianRpIjoiODA5ZmMzY2QtMTU3Mi00NWYxLWFjN2ItYzU0NTQ4NjU1Y2I2IiwiaWRlbnRpdHkiOiIxNjAxMTA3NSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.uyoGJRhz5Ggj1bWh7xlLgyW4gSOCCrErOwHVF4mEzvQ"
temp = "who are you"
header = {
	'Authorization':"Bearer " + temp
}
#Debug Here
url = "http://73.142.229.204"
data = {
	'message' : "who are you? Why do you send me a packet?"
}
######

for i in range(1000):
	print(i)
	html = requests.get(url, headers =header, data = data).content
#html = requests.post(url, headers =header, data = data).content
