from flask import Blueprint

bp_main = Blueprint('main', __name__, url_prefix='/', template_folder='templates', static_folder='static', static_url_path='/main/static')

from app.main import routes
