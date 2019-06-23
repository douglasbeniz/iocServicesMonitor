from app.api import bp_api

@bp_api.route('/iocs', methods=['GET'])
def get_iocs():
    return "list of running IOCs..."
