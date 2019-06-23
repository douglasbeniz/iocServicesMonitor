# -----------------------------------------------------------------------------
# Configuration for iocServicesMonitor
# -----------------------------------------------------------------------------
import os

class Config(object):
    SERVERS = {'ics-iocsad-01':'10.4.3.221', 'ics-banana-evr2.cslab.esss.lu.se':'172.30.242.12', 'ics-iocmach-01.cslab.esss.lu.se':'10.4.0.222', 'det-iocmach-01.cslab.esss.lu.se':'172.30.244.21'}
    # CRITICAL CONFIG VALUE: This tells Flask-Collect where to put our static files!
    # Standard practice is to use a folder named "static" that resides in the top-level of the project directory.
    # You are not bound to this location, however; you may use basically any directory that you wish.
    COLLECT_STATIC_ROOT = os.path.dirname(__file__) + '/static'
    COLLECT_STORAGE = 'flask_collect.storage.file'
