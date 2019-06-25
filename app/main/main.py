# -----------------------------------------------------------------------------
# Utility to monitor systemd services running IOCs as micro-services
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# author: douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
from flask import current_app, render_template
from socket import gethostname

from app.main import bp_main

import os

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------
@bp_main.route('/', methods=['GET', 'POST'])
@bp_main.route('/index', methods=['GET', 'POST'])
def index():
    if current_app.config['SERVERS']:
        servers = []
        for server in current_app.config['SERVERS']:
            servers.append({'class': 'success',
                'title': server,
                'server': server,
                'server_ip':current_app.config['SERVERS'].get(server)})
        return render_template('index.tpl', hostname=gethostname(), servers=servers)
    else:
        return "No server with running IOCs configured!"
