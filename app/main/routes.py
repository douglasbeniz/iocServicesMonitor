from flask import current_app, render_template
#from bottle import auth_basic, template, static_file, TEMPLATE_PATH
#from pam import pam
from simplepam import authenticate as pam_auth
from socket import gethostname


from app.main import bp_main

import os

# -----------------------------------------------------------------------------
# Search for template path
# -----------------------------------------------------------------------------
# template_paths = [ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
#         '/usr/share/sysdweb/templates']
# template_path = [path for path in template_paths if os.access(path, os.R_OK)]
# if template_path == []:
#     raise SystemExit('Templates are missing.')
# TEMPLATE_PATH.insert(0, os.path.join(template_path[0], 'views'))
# static_path = os.path.join(template_path[0], 'static')

# -----------------------------------------------------------------------------
# Define auth function
# -----------------------------------------------------------------------------
def login(user, password):
    #users = config.get('DEFAULT', 'users', fallback=None)
    #if users and not user in users.split(','):
    #    # User not is in the valid user list
    #    return False
    # Validate user with password
    return pam_auth(user, password)

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------
@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
#@auth_basic(login)
def index():
    if current_app.config['SERVERS']:
        #return str(current_app.config['SERVERS'])
        services = []
        for service in current_app.config['SERVERS']:
            #service_status = get_service_action(service, 'status')
            service_status = {'status':'active'}
            if service_status['status'] == 'not-found':
                cls = 'active'
            elif service_status['status'] == 'inactive' or service_status['status'] == 'failed':
                cls = 'danger'
            elif service_status['status'] == 'active':
                cls = 'success'
            else:
                cls = 'warning'
            disabled_start = True if cls == 'active' or cls == 'success' else False
            disabled_stop = True if cls == 'active' or cls == 'danger' else False
            disabled_restart = True if cls == 'active' or cls == 'danger' else False
            services.append({'class': cls,
                'disabled_start': disabled_start,
                'disabled_stop': disabled_stop,
                'disabled_restart': disabled_restart,
                'title': service,
                'service': service,
                'ip':current_app.config['SERVERS'].get(service)})
        return render_template('index.tpl', hostname=gethostname(), services=services)
    else:
        return "No server with running IOCs configured!"

# -----------------------------------------------------------------------------
# Serve static content
# -----------------------------------------------------------------------------
# @bp_main.route('/favicon.ico', methods=['GET'])
# #@auth_basic(login)
# def get_favicon():
#     print(os.path.join(static_path, 'img'))
#     return static_file('favicon.ico', root=os.path.join(static_path, 'img'))

# @bp_main.route('/static/css', methods=['GET'])
# def get_css():
#     #url_for('static', filename='style.css')
#     return redirect(url_for('static/css', filename='/static/css/iocservicesmonitor.css'))

# @bp_main.route('/css/<file>', methods=['GET'])
# #@auth_basic(login)
# def get_css(file):
#     return static_file(file, root=os.path.join(static_path, 'css'))

# @bp_main.route('/fonts/<file>', methods=['GET'])
# #@auth_basic(login)
# def get_fonts(file):
#     return static_file(file, root=os.path.join(static_path, 'fonts'))

# @bp_main.route('/img/<file>', methods=['GET'])
# #@auth_basic(login)
# def get_img(file):
#     return static_file(file, root=os.path.join(static_path, 'img'))

# @bp_main.route('/js/<file>', methods=['GET'])
# #@auth_basic(login)
# def get_js(file):
#     return static_file(file, root=os.path.join(static_path, 'js'))
