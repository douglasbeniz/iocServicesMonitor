from flask import current_app, render_template, abort, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
#from json import loads as json_loads
from socket import gethostname
from app.api import bp_api
from app.api.systemd import systemdBus, Journal, IOC_SERVICES_PREFIX, CONSERVER_PREFIX
#from pam import pam
from simplepam import authenticate as spam_auth


# Authentication
basic_auth = HTTPBasicAuth()


# -----------------------------------------------------------------------------
# Define auth function
# -----------------------------------------------------------------------------
def login(user, password):
    #users = config.get('DEFAULT', 'users', fallback=None)
    #if users and not user in users.split(','):
    #    # User not is in the valid user list
    #    return False
    # Validate user with password
    #return pam().authenticate(user, password)
    return spam_auth(user, password)


# -----------------------------------------------------------------------------
# User and password validation
# -----------------------------------------------------------------------------
@basic_auth.verify_password
def verify_password(username, password):
    return spam_auth(username, password)

# -----------------------------------------------------------------------------
# Show all services on this server and their status
# -----------------------------------------------------------------------------
@bp_api.route('/iocs', methods=['GET'])
@basic_auth.login_required
def get_iocs_list():
    sdbus = systemdBus()
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
        service_title = 'generic-service'
        if IOC_SERVICES_PREFIX in service[0];
            service_title = service[0].replace(IOC_SERVICES_PREFIX, '')
        elif CONSERVER_PREFIX in service[0]:
            service_title = service[0].replace(CONSERVER_PREFIX, '')

        services.append({'class': cls,
            'disabled_start': disabled_start,
            'disabled_stop': disabled_stop,
            'disabled_restart': disabled_restart,
            'title': service_title,
            'service': service[0]})
    return render_template('services.tpl', hostname=gethostname(), services=services)


# -----------------------------------------------------------------------------
# Service and Action to perform over it
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/<service>/<action>', methods=['GET'])
#@auth_basic(login)
@basic_auth.login_required
def get_service_action(service, action):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in str(ioc_services_list):
        if action == 'start':
            response = jsonify({action: 'OK', 'status_code':200}) if sdbus.start_unit(service) else jsonify({action: 'Fail', 'status_code':401})
            return response
        elif action == 'stop':
            response = jsonify({action: 'OK', 'status_code':200}) if sdbus.stop_unit(service) else jsonify({action: 'Fail', 'status_code':401})
            return response
        elif action == 'restart':
            response = jsonify({action: 'OK', 'status_code':200}) if sdbus.restart_unit(service) else jsonify({action: 'Fail', 'status_code':401})
            return response
        elif action == 'reload':
            response = jsonify({action: 'OK', 'status_code':200}) if sdbus.reload_unit(service) else jsonify({action: 'Fail', 'status_code':401})
            return response
        elif action == 'reloadorrestart':
            response = jsonify({action: 'OK', 'status_code':200}) if sdbus.reload_or_restart_unit(service) else jsonify({action: 'Fail', 'status_code':401})
            return response
        elif action == 'status':
            if sdbus.get_unit_load_state(service) != 'not-found':
                response = jsonify({action: str(sdbus.get_unit_active_state(service)), 'status_code':200})
                return response
            else:
                response = jsonify({action: 'not-found', 'status_code':401})
                return response
        elif action == 'journal':
            return get_service_journal(service, 100)
        else:
            response = jsonify({'msg': 'Sorry, but cannot perform \'{}\' action.'.format(action), 'status_code':400})
            return response
    else:
        response = jsonify({'msg': 'Sorry, but \'{}\' is not valid anymore.'.format(service), 'status_code':400})
        return response


# -----------------------------------------------------------------------------
# Get journal of a service with a limit of lines
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/<service>/journal/<lines>', methods=['GET'])
#@auth_basic(login)
@basic_auth.login_required
def get_service_journal(service, lines):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in str(ioc_services_list):
        if sdbus.get_unit_load_state(service) == 'not-found':
            response = jsonify({'journal': 'not-found', 'status_code':401})
            return response
        try:
            lines = int(lines)
        except Exception as e:
            response = jsonify({'msg': '{}'.format(e), 'status_code':500})
            return response
        journal = Journal(service)
        response = jsonify({'journal': journal.get_tail(lines), 'status_code':200})
        return response
    else:
        response = jsonify({'msg': 'Sorry, but \'{}\' is not valid anymore.'.format(service), 'status_code':400})
        return response


def __get_service_journal(service, lines):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in str(ioc_services_list):
        if sdbus.get_unit_load_state(service) == 'not-found':
            response = {'journal': 'not-found'}
            return response
        try:
            lines = int(lines)
        except Exception as e:
            response = {'msg': '{}'.format(e)}
            return response
        journal = Journal(service)
        response = {'journal': journal.get_tail(lines)}
        return response
    else:
        response = {'msg': 'Sorry, but \'{}\' is not valid anymore.'.format(service)}
        return response


# -----------------------------------------------------------------------------
# Get default 100 lines journal of a service
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/journal/<service>', methods=['GET'])
#@auth_basic(login)
@basic_auth.login_required
def get_service_journal_page(service):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in str(ioc_services_list):
        if sdbus.get_unit_load_state(service) == 'not-found':
            abort(400,'Sorry, but service \'{}\' unit not found in system.'.format(service))
        journal_lines = __get_service_journal(service, 100)
        return render_template('journal.tpl', hostname=gethostname(), service=service, journal=journal_lines['journal'])
    else:
        abort(400, 'Sorry, but \'{}\' is not valid anymore.'.format(service))
