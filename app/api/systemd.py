#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the GNU GPLv3 license.

from dbus import SystemBus, SessionBus, Interface, exceptions
from systemd import journal

import subprocess

# -----------------------------------------------------------------------------
# Default parameters
# -----------------------------------------------------------------------------
CONSERVER_CONF              = '/etc/conserver/procs.cf'
DBUS_INTERFACE              = 'org.freedesktop.DBus.Properties'
IOC_SERVICES_PREFIX         = 'ioc@'
IOC_SERVICES_PREFIX_WCHAR   = IOC_SERVICES_PREFIX + '*'
CONSERVER_PREFIX            = 'conserver'
CONSERVER_PREFIX_WCHAR      = IOC_SERVICES_PREFIX + '*'
SYSTEMCTL                   = '/bin/systemctl'
SYSTEMD_BUSNAME             = 'org.freedesktop.systemd1'
SYSTEMD_DIR                 = '/etc/systemd/system'
SYSTEMD_PATH                = '/org/freedesktop/systemd1'
SYSTEMD_MANAGER_INTERFACE   = 'org.freedesktop.systemd1.Manager'
SYSTEMD_UNIT_INTERFACE      = 'org.freedesktop.systemd1.Unit'

class systemdBus(object):
    def __init__(self, user=False):
        self.user = user
        self.bus = SystemBus()
        self.systemd = self.bus.get_object(SYSTEMD_BUSNAME, SYSTEMD_PATH)
        self.manager = Interface(self.systemd, dbus_interface=SYSTEMD_MANAGER_INTERFACE)

    def get_unit_active_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'ActiveState')

    def get_unit_load_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'LoadState')

    def start_unit(self, unit):
        try:
            self.manager.StartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def stop_unit(self, unit):
        try:
            self.manager.StopUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def restart_unit(self, unit):
        try:
            self.manager.RestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_unit(self, unit):
        try:
            self.manager.ReloadUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_or_restart_unit(self, unit):
        try:
            self.manager.ReloadOrRestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def ioc_services_list(self):
        ioc_services_list   = []
        # ---------------------------------------------------------------------
        # first, we check IOCs
        # ---------------------------------------------------------------------
        systemctl_execution = subprocess.Popen([SYSTEMCTL, '--system', '--all', 'list-units', IOC_SERVICES_PREFIX_WCHAR], stdout=subprocess.PIPE)
        response, err       = systemctl_execution.communicate()

        if response:
            parsed_response = str(response).split('\\n')

            for line in parsed_response:
                if IOC_SERVICES_PREFIX in line:
                    ioc_services_list.append(line.split())

        # ---------------------------------------------------------------------
        # and then, conserver
        # ---------------------------------------------------------------------
        systemctl_execution = subprocess.Popen([SYSTEMCTL, '--system', '--all', 'list-units', CONSERVER_PREFIX_WCHAR], stdout=subprocess.PIPE)
        response, err       = systemctl_execution.communicate()

        if response:
            parsed_response = str(response).split('\\n')

            for line in parsed_response:
                if CONSERVER_PREFIX in line:
                    ioc_services_list.append(line.split())

        return ioc_services_list

class Journal(object):
    def __init__(self, unit):
        self.reader = journal.Reader()
        self.reader.add_match(_SYSTEMD_UNIT=unit)

    def get_tail(self, lines):
        self.reader.seek_tail()
        self.reader.get_previous(lines)
        journal_lines = ['{__REALTIME_TIMESTAMP} {MESSAGE}'.format(**value) for value in self.reader]
        self.reader.close()
        return journal_lines
