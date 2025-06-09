from flask import Blueprint, send_from_directory
from appmain import app

shuttle = Blueprint('shuttle', __name__)

@shuttle.route('/shuttle')
def shuttle_info():
    return send_from_directory(app.root_path, 'templates/shuttle_info.html')