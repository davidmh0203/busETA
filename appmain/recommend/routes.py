from flask import Blueprint, render_template
from appmain.recommend.recommend_data import get_recommendation_summary

recommend = Blueprint('recommend', __name__)

@recommend.route('/recommend')
def show_recommend_page():
    data = get_recommendation_summary()
    return render_template("recommend_root.html",
        result_033=data["result_033"],
        result_85=data["result_85"],
        summary=data["summary"]
    )
from flask import request, jsonify
from appmain.recommend.recommend_data import get_recommendation_summary

@recommend.route("/api/recommend")
def api_recommend():
    dest = request.args.get("dest", "삼송역")
    result = get_recommendation_summary(dest)
    return jsonify(result)


