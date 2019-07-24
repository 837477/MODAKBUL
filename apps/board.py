from flask import *
from werkzeug import *
from flask_jwt_extended import *
from PIL import Image
from db_func import *

#import hashlib

BP = Blueprint('board', __name__)

UPLOAD_PATH = "/static/files/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'hwp', 'txt', 'doc', 'xls', 'ppt', 'pptx', 'xlsx', 'docx', 'pdf', 'snd', 'otf', 'art', 'gem', 'wp5', 'wpg', 'wpd', 'wp', 'emg', 'opt', 'info', 'wmf', 'md', 'xla', 'pps', 'dot', 'lbk', 'dcx', 'qdp', 'dat', 'dbf', 'obj', 'rtf', 'dmg', 'zip', '7z', 'rar', 'jar', 'apk', 'pak', 'tar', 'tiff', 'tif', 'eml', 'pic', 'dcx', 'ntf', 'log', 'gz', 'ta.z', 'ta.gz', 'xlw', 'egg', 'ico', 'mpg', 'pif'])
IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

###################################################
#페이지
@BP.route('/gallery')
def imag2222e():
	return render_template('board/index.html')

@BP.route('/posts')
def image2():
	return render_template('board/index2.html')	
###################################################
#포스트 반환

#게시판 목록 불러오기(ex 공지사항, 학생회비 사용내역 등)
@BP.route('/board')
def get_board():
	result = {}
	board = select_board(g.db)

	result.update(
		board = board,
		result = "success")
	return jsonify(result)

#해당 게시판의 글들 불러오기(페이지네이션) (OK)
@BP.route('/posts/<string:tag_string>/<int:page>')
def get_posts_page(tag_string, page):
	result = {}

	tag_list = tag_string.split('_')
	tag_in_post_id = select_tag_in_posts(tag_list)
	
	posts = select_posts_page(g.db, tag_in_post_id, page)

	#포스트 목록들을 불러온다
	for post in posts:
		img_cnt = 0
		file_cnt = 0
		
		#해당 포스트 아이디의 파일들을 불러온다.
		db_files = select_attach(g.db, post['post_id'])

		#파일 개수 파악 시작!!
		for file in db_files:
			#이건 미리보기 파일이라 갯수에 포함X
			if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] != "S#":
				#이미지냐? 아니면 일반파일이냐?
				if file['file_path'].split('.')[-1] in IMG_EXTENSIONS: 
					img_cnt += 1
				else:
					file_cnt += 1
		
		private = select_private_check(g.db, post['post_id'])

		post.update(
			img_cnt = img_cnt,
			file_cnt = file_cnt,
			private = private)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#해당 게시판의 글들 불러오기(전체) (OK)
@BP.route('/posts/<string:tag_string>')
def get_posts_list(tag_string):
	result = {}

	tag_list = tag_string.split('_')
	tag_in_post_id = select_tag_in_posts(tag_list)
	
	posts = select_posts_list(g.db, tag_in_post_id)

	#포스트 목록들을 불러온다
	for post in posts:
		img_cnt = 0
		file_cnt = 0
		
		#날짜 형식 변경
		post['post_date'] = post['post_date'].strftime("%Y년%m월%d일 %H:%M:%S")

		#해당 포스트 아이디의 파일들을 불러온다.
		db_files = select_attach(g.db, post['post_id'])

		#파일 개수 파악 시작!!
		for file in db_files:
			#이건 미리보기 파일이라 갯수에 포함X
			if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] != "S#":
				#이미지냐? 아니면 일반파일이냐?
				if file['file_path'].split('.')[-1] in IMG_EXTENSIONS: 
					img_cnt += 1
				else:
					file_cnt += 1
		
		private = select_private_check(g.db, post['post_id'])

		post.update(
			img_cnt = img_cnt,
			file_cnt = file_cnt,
			private = private)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#해당 게시글 불러오기(단일) (OK)
@BP.route('/post/<int:post_id>')
def get_post(post_id):
	if select_private_check(g.db, post_id) is 1: 
		abort(400)

	result = {}
	post = select_post(g.db, post_id)
	attach = select_attach(g.db, post_id)
	comments = select_comment(g.db, post_id)

	files = []
	#리사이즈 된 파일은 보내줄 필요가 없기 때문에 걸러줌.
	for file in attach:
		if file['file_path'][0:2] != "S#":
			files.append(file['file_path'])

	result_comments = []

	#코맨츠 전체 탐색
	for comment in comments:
		double_comment = []

		#댓글 날짜 형식 변경
		comment['comment_date'] = comment['comment_date'].strftime("%Y년 %m월 %d일 %H:%M:%S")

		#일반 댓글 / 대댓글 판별!
		if comment['comment_parent'] is None:

			#만약 일반이면? 이 일반 댓글의 대댓글의 유/무 탐색
			for d_comment in comments:
				#해당 대댓글이 있으면 대댓글 리스트에 추가!!
				if comment['comment_id'] is d_comment['comment_parent']:
					double_comment.append(d_comment)

			#그리고 해당 댓글 딕셔너리에 대댓글 추가
			comment.update(double_comment = double_comment)
			
			#마지막으로 최정 댓글 리스트에 작업한 댓글 추가
			result_comments.append(comment)

		double_comment = []


	result.update(
		post = post,
		files = files,
		comment = result_comments,
		result = "success")

	return result

#해당 게시글 불러오길(단일, 비밀글 체크용)
@BP.route('/post_private/<int:post_id>')
@jwt_required
def get_post_private(post_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(403)

	post = select_post(g.db, post_id)

	if post['user_id'] is user['user_id'] or user['user_id'] is "ADMIN":
		result = {}

		attach = select_attach(g.db, post_id)
		comment = select_comment(g.db, post_id)
		result.update(
			post = post,
			files = attach,
			comment = comment,
			result = "success")
		return result
	else:
		return jsonify(
			result = "no access")

#갤러리 글들 불러오기 (미리보기 이미지 때문에 따로 API 구현) (OK)
@BP.route('/image/<int:page>')
def image(page):
	result = {}

	tag_in_post_id = select_tag_in_posts(['갤러리'])
	
	g_posts = select_gallery_posts(g.db, tag_in_post_id, page)

	for post in g_posts:
		files = []
		db_files = select_attach(g.db, post['post_id'])
			
		for file in db_files:
			if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] == "S#":
				files.append(file['file_path'])

		post.update(files = files)

	result.update(
		posts = g_posts,
		result = "success")

	return jsonify(result)

#######################################################
#포스트 업로드 및 수정 및 삭제

#게시물 업로드 (OK)
@BP.route('/post_upload', methods=['POST'])
@jwt_required
def post_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	tags = request.form['tags']
	files = request.files.getlist('files')

	tag_list = tags.split('_')

	#게시글 등록을하고 등록된 포스트 아이디를 받아온다.
	post_id = insert_post(g.db, user['user_id'], title, content, anony, tag_list)

	if post_id is None: abort(400)

	else:
		#첨부할 파일이 있는지 확인
		if files is not None:
			for file in files:
				
				#확장자 검사 후,
				#허용불가 확장자면 None!
				#허용이면, 딕셔너리 형태로
				#원본, 리사이즈 이름을 반환
				allow_check = file_name_encode(file.filename)

				if allow_check is not None:
					#DB에 파일 추가.
					path_result = insert_attach(g.db, post_id, allow_check['original'], allow_check['resize_s'])

					if path_result == "success":
						file.save('.' + UPLOAD_PATH + allow_check['original'])
						if allow_check['resize_s'] is not None:
							img = Image.open('.' + UPLOAD_PATH + allow_check['original'])
							resize_img = img.resize((400,300))
							resize_img.save('.' + UPLOAD_PATH + allow_check['resize_s'])
					else:
						return jsonify(result = "Fail save_file")
				else:
					return jsonify(result = "Wrong_file")

		return jsonify(result = "success")

#게시물 수정
@BP.route('/post_update', methods=['POST'])
@jwt_required
def post_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	post_id = request.form['post_id']

	'''
	access = access_check_post(g.db, post_id, user['user_id'])
	#해당 게시글의 작성자와 user토큰과 일치하지 않음, (관리자 제외)
	if access is not 1: abort(400)
	'''

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	files = request.files.getlist('files')

	#수정된 파일이 있을 수 있으니 우선 첨부파일 날리고 본다.
	delete_attach(g.db, post_id)
	
	update_post(g.db, post_id, title, content, anony, user['user_id'])

	#새롭게 받은 파일이 있는지 확인 DB삽입 작업
	if files is not None:
		for file in files:

			allow_check = file_name_encode(file.filename)

			if allow_check is not None:
				#DB에 파일 추가.
				path_result = insert_attach(g.db, post_id, allow_check['original'], allow_check['resize_s'])

				if path_result == "success":
					file.save('.' + UPLOAD_PATH + allow_check['original'])
					if allow_check['resize_s'] is not None:
						img = Image.open('.' + UPLOAD_PATH + allow_check['original'])
						resize_img = img.resize((400,300))
						resize_img.save('.' + UPLOAD_PATH + allow_check['resize_s'])
				else:
					return jsonify(result = "Fail save_file")
			else:
					return jsonify(result = "Wrong_file")

	return jsonify(
		result = "success")

#게시물 삭제
@BP.route('/post_delete', methods=['POST'])
@jwt_required
def post_delete():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	post_id = request.form['post_id']

	access = access_check_post(g.db, post_id, user['user_id'])
	#해당 게시글의 작성자와 user토큰과 일치하지 않음, (관리자 제외)
	if access is not 1: abort(400)

	delete_post(g.db, post_id)

	return jsonify(
		result = "success")

#######################################################
#조회수 / 댓글 / 좋아요 처리

#조회수 증가 (OK)
@BP.route('/view_up/<int:post_id>')
def view_up(post_id):
	result = update_view(g.db, post_id)

	return jsonify(
		result = result)

#좋아요 등록 (OK)
@BP.route('/post_like_up/<int:post_id>')
@jwt_required
def post_like_up(post_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	result = insert_post_like(g.db, post_id, user['user_id'])

	return jsonify(
		result = result)

#좋아요 취소 (OK)
@BP.route('/post_like_down/<int:post_id>')
@jwt_required
def post_like_down(post_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	result = delete_post_like(g.db, post_id, user['user_id'])

	return jsonify(
		result = result)

#댓글 쓰기 (OK)
@BP.route('/comment_upload', methods=['POST'])
@jwt_required
def comment_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	post_id = request.form['post_id']
	comment = request.form['comment']
	anony = request.form['anony']
	comment_id = request.form['comment_id']

	if comment_id is 0:
		comment_id = "NULL"
	

	result = insert_comment(g.db, post_id, user['user_id'], comment, anony, comment_id)

	return jsonify(
		result = result)

#댓글 수정 (보류)
@BP.route('/comment_update', methods=['POST'])
@jwt_required
def comment_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	comment_id = request.form['comment_id']

	'''
	access = access_check_comment(g.db, comment_id, user['user_id'])
	#해당 게시글의 작성자와 user토큰과 일치하지 않음, (관리자 제외)
	if access is not 1: abort(400)
	'''

	comment = request.form['comment']
	anony = request.form['anony']

	result = update_comment(g.db, comment_id, comment, anony, user['user_id'])

	return jsonify(
		result = result)

#댓글 삭제
@BP.route('/comment_delete', methods=['POST'])
@jwt_required
def comment_delete():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	comment_id = request.form['comment_id']

	access = access_check_comment(g.db, comment_id, user['user_id'])
	#해당 게시글의 작성자와 user토큰과 일치하지 않음, (관리자 제외)
	if access is not 1: abort(400)

	result = delete_comment(g.db, comment_id)

	return jsonify(
		result = result)

#함수 #########################################################
'''
def to_hash(pw):
	sha = hashlib.new('md5')
	sha.update(pw.encode('utf-8'))
	print(sha.hexdigest())
	return sha.hexdigest()
'''

#파일 이름 변환
def file_name_encode(file_name):
	#허용 확장자 / 길이인지 확인.
	if secure_filename(file_name).split('.')[-1] in ALLOWED_EXTENSIONS and len(file_name) < 240:

		#원본 파일!
		path_name = str(datetime.today().strftime("%Y%m%d%H%M%S%f")) + '_' + file_name

		#이미지 리사이즈 파일!
		path_name_S = None

		if secure_filename(file_name).split('.')[-1] in IMG_EXTENSIONS:
			path_name_S = 'S#' + path_name 

		return {"original": path_name, "resize_s": path_name_S}
	
	else:
		return None



