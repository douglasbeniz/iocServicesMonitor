from flask import current_app, render_template
#from pam import pam
from simplepam import authenticate as pam_auth
from socket import gethostname


from app.main import bp_main

import os


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
        servers = []
        for server in current_app.config['SERVERS']:
            servers.append({'class': 'success',
                'title': server,
                'server': server,
                'server_ip':current_app.config['SERVERS'].get(server)})
        return render_template('index.tpl', hostname=gethostname(), servers=servers)
    else:
        return "No server with running IOCs configured!"
