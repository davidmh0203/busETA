from flask import Blueprint, send_from_directory

from appmain import app

recommend = Blueprint('recommend', __name__)
@recommend.route('/recommend')
def reccomend():
    return send_from_directory(app.root_path, 'templates/recommend_root.html')
