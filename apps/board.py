from flask import *
from werkzeug import *
from flask_jwt_extended import *
from PIL import Image
from db_func import *
from word_filter import *

BP = Blueprint('board', __name__)

UPLOAD_PATH = "/static/files/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'hwp', 'txt', 'doc', 'xls', 'ppt', 'pptx', 'xlsx', 'docx', 'pdf', 'snd', 'otf', 'art', 'gem', 'wp5', 'wpg', 'wpd', 'wp', 'emg', 'opt', 'info', 'wmf', 'md', 'xla', 'pps', 'dot', 'lbk', 'dcx', 'qdp', 'dat', 'dbf', 'obj', 'rtf', 'dmg', 'zip', '7z', 'rar', 'jar', 'apk', 'pak', 'tar', 'tiff', 'tif', 'eml', 'pic', 'dcx', 'ntf', 'log', 'gz', 'ta.z', 'ta.gz', 'xlw', 'egg', 'ico', 'mpg', 'pif'}
IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

#######################################################
#페이지 URL#############################################
@BP.route('/board/')
def board():
   return render_template('board/board.html')

@BP.route('/gallery')
def gallery():
   return render_template('board/image.html')

@BP.route('/intro')
def intro():
   return render_template('board/intro.html')

@BP.route('/v')
def postpage():
   return render_template('board/postpage.html')
#######################################################
#보드 / 포스트 반환#############################################

#보드(메뉴) 목록 디비 원본 (OK)
@BP.route('/get_boards_origin')
@jwt_required
def get_boards_origin():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#관리자 아니면 접근 거절!
	if not check_admin(g.db, user['user_id']): 
		abort(400)

	result = {}
	boards = select_boards(g.db)

	result.update(
		result = "success",
		boards = boards)

	return jsonify(result)

#보드(메뉴) 목록 불러오기 (OK)
@BP.route('/get_boards')
@jwt_optional
def get_boards():
	result = {}
	boards = select_boards(g.db)

	#토큰이 있으면?
	if get_jwt_identity():
		user = select_user(g.db, get_jwt_identity())
		if user is None: abort(400)

		#로그 기록
		insert_log(g.db, user['user_id'], request.url_rule)

		#관리자이면?
		if check_admin(g.db, user['user_id']):
			for board in boards:
				board['board_access'] = 1
		#일반 유저이면?
		else:
			for board in boards:
				if board['board_access'] == 0:
					board['board_access'] = 1
				else:
					board['board_access'] = 0
	else:
		for board in boards:
				board['board_access'] = 0

	result.update(
		boards = boards,
		result = "success")

	return jsonify(result)

#보드(메뉴) 단일 정보 불러오기 (OK)
@BP.route('/get_board/<string:board_url>')
@jwt_optional
def get_board(board_url):
	result = {}

	board = select_board(g.db, board_url)

	if board is None:
		return jsonify(reuslt = "board is empty")

	#토큰이 있으면?
	if get_jwt_identity():
		user = select_user(g.db, get_jwt_identity())
		if user is None: abort(400)

		#로그 기록
		insert_log(g.db, user['user_id'], request.url_rule)

		#관리자이면?
		if check_admin(g.db, user['user_id']):
			if board_url in {'대외활동', '대외활동_공모전', '대외활동_취업'}:
				board['board_access'] = 0
			else:
				board['board_access'] = 1
		#일반 유저이면?
		else:
			if board['board_access'] == 0:
				board['board_access'] = 1
			else:
				board['board_access'] = 0
	else:
		board['board_access'] = 0
	

	result.update(
		board = board,
		result = "success")
	return jsonify(result)
	
#특정 게시판의 글들 불러오기(페이지네이션) (OK)
@BP.route('/get_posts/<string:tag_string>/<int:page>')
def get_posts_page(tag_string, page):
	result = {}

	#태그 스플릿 작업
	tag_list = tag_string.split('_')
	tag_in_post_id = select_tag_in_posts(tag_list)
	
	#게시물들 불러오기.
	posts = select_posts_page(g.db, tag_in_post_id, page)

	#포스트 목록들을 불러온다
	for post in posts:
		img_cnt = 0
		file_cnt = 0
		
		#해당 포스트 아이디의 파일들을 불러온다.
		db_files = select_attach(g.db, post['post_id'])

		#날짜 형식 변경
		post['post_date'] = post['post_date'].strftime("%Y년 %m월 %d일 %H:%M:%S")

		#파일 개수 파악 시작!!
		for file in db_files:
			#이건 미리보기 파일이라 갯수에 포함X
			if file['file_path'][0:2] != "S-":
				#이미지냐? 아니면 일반파일이냐?
				if file['file_path'].split('.')[-1] in IMG_EXTENSIONS: 
					img_cnt += 1
				else:
					file_cnt += 1

		post.update(
			img_cnt = img_cnt,
			file_cnt = file_cnt)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#특정 게시판의 글들 불러오기(전체) (OK)
@BP.route('/get_posts/<string:tag_string>')
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
		post['post_date'] = post['post_date'].strftime("%Y년 %m월 %d일 %H:%M:%S")

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

		post.update(
			img_cnt = img_cnt,
			file_cnt = file_cnt)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#갤러리 글들 불러오기 (미리보기 이미지 때문에 따로 API 구현) (OK)
@BP.route('/get_image/<int:page>')
def get_image(page):
	result = {}

	tag_in_post_id = select_tag_in_posts(['갤러리'])
	
	g_posts = select_gallery_posts(g.db, tag_in_post_id, page)

	for post in g_posts:
		files = []
		db_files = select_attach(g.db, post['post_id'])
			
		for file in db_files:
			if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] == "S-":
				files.append(file['file_path'])

		post.update(files = files)

	result.update(
		posts = g_posts,
		result = "success")

	return jsonify(result)

#단일 포스트 불러오기 (공개글 / 비공개글 공통 URL) (OK)
@BP.route('/get_post/<int:post_id>')
@jwt_optional
def get_post(post_id):
	private = secret_post_check(g.db, post_id)
	result = {"property": 0}

	#토큰 유무 확인
	if get_jwt_identity():
		#해당 토큰으로 유저 정보를 불러오고
		user = select_user(g.db, get_jwt_identity())
		if user is None: abort(400)

		#로그 기록
		insert_log(g.db, user['user_id'], request.url_rule)

		#비밀글이면?
		if private:
			#Admin 체크
			if check_admin(g.db, user['user_id']):
				post = get_post_func(post_id)
				result.update(admin = 1)
			#작성자 본인이라면?
			elif select_author_check(g.db, post_id, user['user_id']):
				post = get_post_func(post_id)
				result['property'] = 1
			#관리자 / 작성자도 아니면 뻐큐
			else:
				return jsonify(result = "do not access")
		#비밀글이 아니요!
		else:
			post = get_post_func(post_id)

			if check_admin(g.db, user['user_id']):
				result.update(admin = 1)

			if select_author_check(g.db, post_id, user['user_id']):
				result['property'] = 1
	else:	
		#비밀글이면?
		if private:
			return jsonify(result = "do not access")
		else:
			post = get_post_func(post_id)
	
	result.update(
		post,
		result = "success")

	return jsonify(result)

#단일 포스트 불러오기(포스트 정보 가져오는 함) (OK)
def get_post_func(post_id):
	result = {}
	post = select_post(g.db, post_id)

	if post is None:
		return jsonify(result = "define post")

	attach = select_attach(g.db, post_id)
	comments = select_comment(g.db, post_id)

	#프론트의 요구로 날짜 형식 변형
	post['post_date'] = post['post_date'].strftime("%Y년 %m월 %d일 %H:%M:%S")

	files = []
	#리사이즈 된 파일은 보내줄 필요가 없기 때문에 걸러줌.
	for file in attach:
		if file['file_path'][0:2] != "S-":
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

#######################################################
#포스트 업로드 및 수정 및 삭제###############################

#게시물 업로드 (OK)
@BP.route('/post_upload', methods=['POST'])
@jwt_required
def post_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	secret = request.form['secret']
	tags = request.form['tags']
	files = request.files.getlist('files')

	#게시글 작성권한 확인
	if check_admin(g.db, user['user_id']):
		pass
	else:
		insert_check = insert_access_check_post(g.db, tags)
		if insert_check is None:
			return jsonify(result = "define board")
		#관리자가 아닌데, 이 보드의 접근권한이 관리자부터면?
		elif insert_check['board_access'] == 1:
			return jsonify(result = "do not access")

	#욕 필터
	if check_word_filter(title):
		return jsonify(result = "unavailable word")
	if check_word_filter(content):
		return jsonify(result = "unavailable word")
	tag_list = tags.split('_')

	#익명 글이면?
	anony = int(anony)
	if anony:
		#게시글 등록을하고 등록된 포스트 아이디를 받아온다.
		post_id = insert_post(g.db, "anony", title, content, anony, secret, tag_list)
	else:
		post_id = insert_post(g.db, user['user_id'], title, content, anony, secret, tag_list)

	if post_id is None: abort(400)
	
	else:
		#첨부할 파일이 있는지 확인
		if files:
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
						delete_post(g.db, post_id)
						return jsonify(result = "fail")
				else:
					return jsonify(result = "wrong file")

		return jsonify(result = "success")

#게시물 수정 (OK)
@BP.route('/post_update', methods=['POST'])
@jwt_required
def post_update():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	post_id = request.form['post_id']

	#포스트 주인 확인 (수정은 관리자도 못함)
	if not select_author_check(g.db, post_id, user['user_id']):
		return jsonify(result = "you are not access")

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	secret = request.form['secret']
	files = request.files.getlist('files')

	#욕 필터
	if check_word_filter(title):
		return jsonify(result = "unavailable word")
	if check_word_filter(content):
		return jsonify(result = "unavailable word")

	#수정된 파일이 있을 수 있으니 우선 첨부파일 날리고 본다.
	delete_attach(g.db, post_id)
	
	result = update_post(g.db, post_id, title, content, anony, secret, user['user_id'])

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
		result = result)

#게시물 삭제 (OK)
@BP.route('/post_delete/<int:post_id>')
@jwt_required
def post_delete(post_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	#삭제 권환이 있는 유저인지 확인 (관리자 토큰이면 허용됨)
	if not delete_access_check_post(g.db, post_id, user['user_id']):
		return jsonify(result = "do not access")

	result = delete_post(g.db, post_id)

	return jsonify(
		result = result)

#######################################################
#조회수 / 댓글 / 좋아요 처리################################

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

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	result = insert_post_like(g.db, post_id, user['user_id'])

	return jsonify(
		result = result)

#좋아요 취소 (OK)
@BP.route('/post_like_down/<int:post_id>')
@jwt_required
def post_like_down(post_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	result = delete_post_like(g.db, post_id, user['user_id'])

	return jsonify(
		result = result)

#댓글 쓰기 (OK)
@BP.route('/comment_upload', methods=['POST'])
@jwt_required
def comment_upload():
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	post_id = request.form['post_id']
	comment = request.form['comment']
	anony = request.form['anony']
	comment_id = request.form['comment_id']

	#욕 필터
	if check_word_filter(comment):
		return jsonify(result = "unavailable word")

	if comment_id == "0":
		comment_id = None
	
	anony = int(anony)
	#익명이냐?
	if anony:
		result = insert_comment(g.db, post_id, "anony", comment, anony, comment_id)
	else:
		result = insert_comment(g.db, post_id, user['user_id'], comment, anony, comment_id)

	return jsonify(
		result = result)

#댓글 삭제 (OK)
@BP.route('/comment_delete/<int:comment_id>')
@jwt_required
def comment_delete(comment_id):
	user = select_user(g.db, get_jwt_identity())
	if user is None: abort(400)

	#로그 기록
	insert_log(g.db, user['user_id'], request.url_rule)

	access = delete_access_check_comment(g.db, comment_id, user['user_id'])

	#해당 게시글의 작성자와 user토큰과 일치하지 않음, (관리자 제외)
	if not access: abort(400)

	result = delete_comment(g.db, comment_id)

	return jsonify(
		result = result)

#######################################################
#함수 ##################################################

#파일 이름 변환
def file_name_encode(file_name):
	#허용 확장자 / 길이인지 확인.
	if secure_filename(file_name).split('.')[-1].lower() in ALLOWED_EXTENSIONS and len(file_name) < 240:

		#원본 파일!
		path_name = str(datetime.today().strftime("%Y%m%d%H%M%S%f")) + '_' + file_name

		#이미지 리사이즈 파일!
		path_name_S = None

		if secure_filename(file_name).split('.')[-1].lower() in IMG_EXTENSIONS:
			path_name_S = 'S-' + path_name 

		return {"original": path_name, "resize_s": path_name_S}
	
	else:
		return None



