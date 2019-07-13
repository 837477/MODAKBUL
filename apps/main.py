from flask import Blueprint, render_template

BP = Blueprint('main', __name__)

@BP.route('/')
def main_home():
	return render_template('main/index.html')