from flask import Blueprint, render_template
from appmain.recommend.recommend_data import get_recommendation_summary

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    summary = get_recommendation_summary()
    return render_template('index.html', summary=summary)
