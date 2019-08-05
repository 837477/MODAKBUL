from flask import *
from werkzeug import *
from flask_jwt_extended import *
from operator import itemgetter
from db_func import *
from word_filter import *

BP = Blueprint('search', __name__)
IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
#검색 (OK)
@BP.route('/search/<string:topic>')
def search(topic):
	result = {}

	#욕 필터
	if check_word_filter(topic):
		return jsonify(result = "unavailable word")

	topic_list = topic.split('&')
	posts = select_search(g.db, topic_list)
	
	filter_posts = []

	for post in posts:
		#비밀글은 그냥 모든 작업을 건너 뛴다.
		private = secret_post_check(g.db, post['post_id'])
		if private == 1:
			continue

		#날짜 형식 변경
		post['post_date'] = post['post_date'].strftime("%Y년 %m월 %d일 %H:%M:%S")

		#해당 포스트 아이디의 파일들을 불러온다.
		db_files = select_attach(g.db, post['post_id'])
		img_cnt = 0
		file_cnt = 0

		#파일 개수 파악 시작!!
		for file in db_files:
			#이건 미리보기 파일이라 갯수에 포함X
			if file['file_path'][0:2] != "S-":
				#이미지냐? 아니면 일반파일이냐?
				if file['file_path'].split('.')[-1] in IMG_EXTENSIONS: 
					img_cnt += 1
				else:
					file_cnt += 1
		#빈도수 체크
		count = 0
		for topic in topic_list:
			count += post['post_title'].count(topic)
			count += post['post_content'].count(topic)
			if post['user_name'] is not None:
				count += post['user_name'].count(topic)

		post.update(
			frequency = count,
			img_cnt = img_cnt,
			file_cnt = file_cnt)

		#모든 작업이 끝난 최종 글들만 이 리스트에 추가됨.
		filter_posts.append(post)

	#빈도수 / 날짜로 정렬!
	filter_posts = sorted(filter_posts, key=itemgetter('frequency', 'post_date'), reverse = True)
	filter_posts = tuple(filter_posts)
	
	result.update(
		posts = filter_posts,
		result = "success")
	return jsonify(result)
