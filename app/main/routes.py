from app.main import bp_main

@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
def index():
    return "Index!"
