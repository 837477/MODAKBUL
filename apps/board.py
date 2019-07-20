from flask import *
from werkzeug import *
from flask_jwt_extended import *
from PIL import Image
import hashlib
from datetime import datetime
from db_func import *

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

#게시판 반환(ex 공지사항, 학생회비 사용내역 등)
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
	post_in_tag_SQL = select_posts_in_tag(tag_list)
	
	posts = select_posts_page(g.db, post_in_tag_SQL, page)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#해당 게시판의 글들 불러오기(전체) (OK)
@BP.route('/posts/<string:tag_string>')
def get_posts_list(tag_string):
	result = {}
	
	tag_list = tag_string.split('_')
	post_in_tag_SQL = select_posts_in_tag(tag_list)
	
	posts = select_posts_list(g.db, post_in_tag_SQL)

	result.update(
		posts = posts,
		result = "success")
	return jsonify(result)

#해당 게시글 불러오기(단일) (OK)
@BP.route('/post/<int:post_id>')
def get_post(post_id):
	result = {}
	post = select_post(g.db, post_id)
	result.update(
		post = post,
		result = "success")
	return result

#게시물 업로드 (OK)
@BP.route('/post_upload', methods=['POST'])
@jwt_required
def post_upload():
	user = select_user_id(g.db, get_jwt_identity())
	if user is None: abort(403)

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	tages = request.form['tages']
	files = request.files.getlist('files')

	tag_list = tages.split('_')

	#게시글 등록을하고 등록된 포스트 아이디를 받아온다.
	post_id = insert_post(g.db, user['user_id'], title, content, anony, tag_list)

	if post_id is None:
		return jsonify(result = "Fail")
	else:
		#첨부할 파일이 있는지 확인
		if files is not None:
			for file in files:
				#확장자 검색!
				if secure_filename(file.filename).split('.')[-1] in ALLOWED_EXTENSIONS:
					path_name = to_hash(user['user_id'] + datetime.today().strftime("%Y%m%d%H%M%S") + file.filename)
					path_name_S = None #그냥 만들어둠

					#이미지 인지 파악
					if secure_filename(file.filename).split('.')[-1] in IMG_EXTENSIONS:
						path_name_S = 'S_' + path_name + '.' + secure_filename(file.filename).split('.')[-1]
					
					path_name += '.' + secure_filename(file.filename).split('.')[-1]

					#DB에 파일경로 추가.
					path_result = insert_attach(g.db, post_id, path_name, path_name_S)

					if path_result == "success":
						file.save('.' + UPLOAD_PATH + path_name)
						if path_name_S is not None:
							img = Image.open('.' + UPLOAD_PATH + path_name)
							resize_img = img.resize((400,300))
							resize_img.save('.' + UPLOAD_PATH + path_name_S)
					else:
						return jsonify(result = "Fail insert_file")
				else:
					return jsonify(result = "Wrong_extension")

		return jsonify(result = "success")

#갤러리 글 목록 (OK)
@BP.route('/image/<int:page>')
def image(page):
	result = {}

	post_in_tag_SQL = select_posts_in_tag(['갤러리'])
	
	g_posts = select_gallery_posts(g.db, post_in_tag_SQL, page)

	for post in g_posts:
		files = []
		db_files = select_files(g.db, post['post_id'])
			
		for file in db_files:
			if file['file_path'].split('.')[-1] in IMG_EXTENSIONS and file['file_path'][0:2] == "S_":
				files.append(file['file_path'])

		post.update(files = files)

	result.update(
		posts = g_posts,
		result = "success")

	return jsonify(result)


#함수 #########################################################

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_hash(pw):
	sha = hashlib.new('md5')
	sha.update(pw.encode('utf-8'))
	print(sha.hexdigest())
	return sha.hexdigest()


