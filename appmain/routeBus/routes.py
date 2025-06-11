from flask import Blueprint, send_from_directory, jsonify
from appmain import app
from appmain.routeBus.bus_api import get_recommendation

routeBus = Blueprint('routeBus', __name__)

@routeBus.route('/routeBus')
def routeBus_info():
    return send_from_directory(app.root_path, 'templates/routeBus_info.html')


@routeBus.route("/api/arrival", methods=["GET"])
def api_arrival():
    results = get_recommendation()
    return jsonify(results)

