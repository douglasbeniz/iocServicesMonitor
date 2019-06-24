from flask import current_app, render_template
from socket import gethostname
from app.api import bp_api
from app.api.systemd import systemdBus, Journal, IOC_SERVICES_PREFIX


# -----------------------------------------------------------------------------
# Show all services on this server and their status
# -----------------------------------------------------------------------------
@bp_api.route('/iocs', methods=['GET'])
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
        services.append({'class': cls,
            'disabled_start': disabled_start,
            'disabled_stop': disabled_stop,
            'disabled_restart': disabled_restart,
            'title': service[0].replace(IOC_SERVICES_PREFIX, ''),
            'service': service[0]})
    return render_template('services.tpl', hostname=gethostname(), services=services)


# -----------------------------------------------------------------------------
# Service and Action to perform over it
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/<service>/<action>', methods=['GET'])
#@auth_basic(login)
def get_service_action(service, action):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in ioc_services_list:
        if action == 'start':
            return {action: 'OK'} if sdbus.start_unit(service) else {action: 'Fail'}
        elif action == 'stop':
            return {action: 'OK'} if sdbus.stop_unit(service) else {action: 'Fail'}
        elif action == 'restart':
            return {action: 'OK'} if sdbus.restart_unit(service) else {action: 'Fail'}
        elif action == 'reload':
            return {action: 'OK'} if sdbus.reload_unit(service) else {action: 'Fail'}
        elif action == 'reloadorrestart':
            return {action: 'OK'} if sdbus.reload_or_restart_unit(service) else {action: 'Fail'}
        elif action == 'status':
            if sdbus.get_unit_load_state(service) != 'not-found':
                return {action: str(sdbus.get_unit_active_state(service))}
            else:
                return {action: 'not-found'}
        elif action == 'journal':
            return get_service_journal(service, 100)
        else:
            response.status = 400
            return {'msg': 'Sorry, but cannot perform \'{}\' action.'.format(action)}
    else:
        response.status = 400
        return {'msg': 'Sorry, but \'{}\' is not defined in config.'.format(service)}


# -----------------------------------------------------------------------------
# Get journal of a service with a limit of lines
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/<service>/journal/<lines>', methods=['GET'])
#@auth_basic(login)
def get_service_journal(service, lines):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in ioc_services_list:
        if get_service_action(service, 'status')['status'] == 'not-found':
            return {'journal': 'not-found'}
        try:
            lines = int(lines)
        except Exception as e:
            response.status = 500
            return {'msg': '{}'.format(e)}
        unit = config.get(service, 'unit')
        journal = Journal(unit)
        return {'journal': journal.get_tail(lines)}
    else:
        response.status = 400
        return {'msg': 'Sorry, but \'{}\' is not defined in config.'.format(service)}


# -----------------------------------------------------------------------------
# Get default 100 lines journal of a service
# -----------------------------------------------------------------------------
@bp_api.route('/iocs/journal/<service>', methods=['GET'])
#@auth_basic(login)
def get_service_journal_page(service):
    sdbus = systemdBus()
    ioc_services_list = sdbus.ioc_services_list()

    if service in ioc_services_list:
        if get_service_action(service, 'status')['status'] == 'not-found':
            abort(400,'Sorry, but service \'{}\' unit not found in system.'.format(config.get(service, 'title')))
        journal_lines = get_service_journal(service, 100)
        return render_template('journal.tpl', hostname=gethostname(), service=service, journal=journal_lines['journal'])
    else:
        abort(400, 'Sorry, but \'{}\' is not defined in config.'.format(service))