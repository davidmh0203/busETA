import json
from flask import Blueprint, send_from_directory, jsonify
from appmain import app

shuttle = Blueprint('shuttle', __name__)

@shuttle.route('/shuttle')
def shuttle_info():
    return send_from_directory(app.root_path, 'templates/shuttle_info.html')

@shuttle.route('/api/shuttle')
def shuttle_api():
    with open('appmain/static/data/shuttle_backseck.json', encoding='utf-8') as f1:
        b_data = json.load(f1)['data']
    with open('appmain/static/data/shuttle_samsong.json', encoding='utf-8') as f2:
        s_data = json.load(f2)['data']

    # 백석 셔틀
    baekseok = []
    for row in b_data:
        baekseok.append({
            "go": row[1],
            "back": row[4],
            "note": row[5]
        })

    # 삼송 셔틀
    samsong = []
    for row in s_data:
        samsong.append({
            "wonheung": row[1] or "-",
            "samsong": row[2] or "-",
            "campus": row[3] or "-",
            "back": row[5] or "-",
            "note": row[6] or "-"
        })

    return jsonify({
        "baekseok": baekseok,
        "samsong": samsong
    })
