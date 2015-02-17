"""Blueprint for angular js app"""
from flask import Blueprint

bp = Blueprint(
    'ngapp', __name__,
    static_url_path='/app',
    static_folder='../../client/dist')


@bp.route('/app/', methods=['GET'])
def home():
    return bp.send_static_file('index.html')
