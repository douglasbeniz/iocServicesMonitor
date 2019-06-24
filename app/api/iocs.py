from flask import current_app, render_template
from socket import gethostname
from app.api import bp_api
from app.api.systemd import systemdBus, Journal

@bp_api.route('/iocs/v1', methods=['GET'])
def get_iocs_list():
    #return "list of running IOCs..."
    sdbus = systemdBus(True)
    ioc_services_list = sdbus.ioc_services_list()
    # header of listed services:
    #   > UNIT          [0]
    #   > LOAD          [1]
    #   > ACTIVE        [2]
    #   > SUB           [3]
    #   > DESCRIPTION   [4:]
    services = []
    for service in ioc_services_list:
        server_status = { 'status':service[1] if service[1] == 'not-found' else service[2] }
        if server_status['status'] == 'not-found':
            cls = 'active'
        elif server_status['status'] == 'inactive' or server_status['status'] == 'failed':
            cls = 'danger'
        elif server_status['status'] == 'active':
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
            'title': gethostname(),
            'service': service})
    return render_template('services.tpl', hostname=gethostname(), services=services)

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/v1/<server>', methods=['GET'])
#@auth_basic(login)
def get_iocs(server):
    if current_app.config['SERVERS']:
        server_ip = current_app.config['SERVERS'].get(server)
        """
        for server in current_app.config['SERVERS']:
            #server_status = get_server_action(server, 'status')
            server_status = {'status':'active'}
            if server_status['status'] == 'not-found':
                cls = 'active'
            elif server_status['status'] == 'inactive' or server_status['status'] == 'failed':
                cls = 'danger'
            elif server_status['status'] == 'active':
                cls = 'success'
            else:
                cls = 'warning'
            disabled_start = True if cls == 'active' or cls == 'success' else False
            disabled_stop = True if cls == 'active' or cls == 'danger' else False
            disabled_restart = True if cls == 'active' or cls == 'danger' else False
            servers.append({'class': cls,
                'disabled_start': disabled_start,
                'disabled_stop': disabled_stop,
                'disabled_restart': disabled_restart,
                'title': server,
                'server': server,
                'server_ip':current_app.config['SERVERS'].get(server)})
        return render_template('index.tpl', hostname=gethostname(), servers=servers)
        """
        return "List of running IOCs at %s (%s)" % (server, server_ip)
    else:
        return "No server with running IOCs configured!"
