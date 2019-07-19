from flask import *
from werkzeug import *
from flask_jwt_extended import *
import hashlib
from datetime import datetime
from db_func import *

BP = Blueprint('board', __name__)

UPLOAD_PATH = "/static/img_save/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'hwp', 'txt', 'doc', 'xls', 'ppt', 'pptx', 'xlsx', 'docx', 'pdf', 'snd', 'otf', 'art', 'gem', 'wp5', 'wpg', 'wpd', 'wp', 'emg', 'opt', 'info', 'wmf', 'md', 'xla', 'pps', 'dot', 'lbk', 'dcx', 'qdp', 'dat', 'dbf', 'obj', 'rtf', 'dmg', 'zip', '7z', 'rar', 'jar', 'apk', 'pak', 'tar', 'tiff', 'tif', 'eml', 'pic', 'dcx', 'ntf', 'log', 'gz', 'ta.z', 'ta.gz', 'xlw', 'egg', 'ico', 'mpg', 'pif'])

###################################################
#페이지
@BP.route('/gallery')
def image():
	return render_template('board/index.html')
###################################################

#게시판 반환(ex 공지사항, 학생회비 사용내역 등)
@BP.route('/board')
def get_board():
	board = select_board(g.db)
	return jsonify(board)

#해당 게시판의 글들 불러오기
@BP.route('/posts/<string:tag_string>')
def get_posts_list(tag_string):
	tag_list = tag_string.split('_')
	post_in_tag_SQL = select_posts_id_SQL(tag_list)
	result = select_posts_list(g.db, post_in_tag_SQL)
	return jsonify(result)

#게시물 업로드
@BP.route('/post_upload', methods=['POST'])
@jwt_required
def post_upload():
	user = select_user_id(g.db, get_jwt_identity())

	if user is None: abort(403)

	title = request.form['title']
	content = request.form['content']
	anony = request.form['anony']
	files = request.files.getlist('files')

	if files is not None:
		post_id = insert_post(g.db, user['user_id'], title, content, anony)

		if post_id is not None:

			for file in files:
				if secure_filename(file.filename).split('.')[-1] in ALLOWED_EXTENSIONS:
					
					path_name = to_hash(user['user_id'] + datetime.today().strftime("%Y%m%d%H%M%S") + file.filename) + '.' + secure_filename(file.filename).split('.')[-1]
					
					print(path_name)

					path_result = insert_attach(g.db, post_id, path_name)
					if path_result == "success":
						file.save('.' + UPLOAD_PATH + path_name)
					else:
						return jsonify(result = "Fail insert_file")
				else:
					return jsonify(result = "Wrong_extension")
		else:
			return jsonify(result = "Fail insert_post")
	else:
		post_id = insert_post(g.db, user['user_id'], title, content, anony)

	if post_id is not None:
		return jsonify(result = "success")
	else:
		return jsonify(result = "Fail")


'''
@BP.route('/image', method=['POST'])
def get_image():
	image_start = request.form['cnt_start']
	image_start = request.form['cnt_end']
'''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_hash(pw):
	sha = hashlib.new('md5')
	sha.update(pw.encode('utf-8'))
	print(sha.hexdigest())
	return sha.hexdigest()


