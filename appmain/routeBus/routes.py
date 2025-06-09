from flask import Blueprint, send_from_directory
from appmain import app
routeBus = Blueprint('routeBus', __name__)

@routeBus.route('/routeBus')
def routeBus_info():
    return send_from_directory(app.root_path, 'templates/routeBus_info.html')


