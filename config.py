# -----------------------------------------------------------------------------
# Utility to monitor systemd services running IOCs as micro-services
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# author: douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
# Configuration for iocServicesMonitor
# -----------------------------------------------------------------------------

class Config(object):
    SERVERS = { 'ics-iocsad-01':'10.4.3.221',
        'ics-banana-evr2.cslab.esss.lu.se':'172.30.242.12',
        'ics-iocmach-01.cslab.esss.lu.se':'172.30.244.12',
        'det-iocmach-01.cslab.esss.lu.se':'172.30.244.21' }

