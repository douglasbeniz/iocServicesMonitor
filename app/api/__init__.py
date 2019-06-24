from flask import Blueprint

bp_api = Blueprint('api', __name__, url_prefix='/api/v1', template_folder='templates', static_folder='static', static_url_path='/main/static')

from app.api import iocs