#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from global_func import *

#apps
import main, auth, board, vote, search, admin, analysis
import error

application = Flask(__name__, instance_relative_config=True)
cors = CORS(application)

#Debug or Release
application.config.update(
		DEBUG = True,
		JWT_SECRET_KEY = 'secret string',
		MAX_CONTENT_LENGTH = 16 * 1024 * 1024,
		UPLOAD_FOLDER = './img_save/'
	)
jwt = JWTManager(application)

def main_app(test_config = None):
	#DB초기화
	init_db()
	#백그라운드 작업
	schedule_init()
	#페이지들
	application.register_blueprint(main.BP)
	application.register_blueprint(auth.BP)
	application.register_blueprint(board.BP)
	application.register_blueprint(vote.BP)
	application.register_blueprint(search.BP)
	application.register_blueprint(admin.BP)
	application.register_blueprint(analysis.BP)
	application.register_blueprint(error.BP)

@application.before_request
def before_request():
	get_db()

@application.teardown_request
def teardown_request(exception):
	close_db()

main_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)

    