# -----------------------------------------------------------------------------
# Utility to monitor systemd services running IOCs as micro-services
# -----------------------------------------------------------------------------
# ESS ERIC - ICS HWI group
# -----------------------------------------------------------------------------
# author: douglas.bezerra.beniz@esss.se
# -----------------------------------------------------------------------------
from app import create_app

# in the case of a 'server' to the list of IOC servers
iocServicesMonitor = create_app(register_main=True)
# in the case of a 'server' where IOCs are running
#iocServicesMonitor = create_app(register_api=True)