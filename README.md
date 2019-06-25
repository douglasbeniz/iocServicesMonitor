# iocServicesMonitor
Utility to monitor systemd services running IOCs as micro-services

### ESS ERIC - ICS HWI group

## Installation

### Prerequisites

* `glib2-devel`;
* `python3*-devel`;
* `libdbus*-dev` (Ubuntu/Debian), `dbus-devel` (CentOS);
* `libsystemd-dev` (Ubuntu/Debian), `systemd-devel` (CentOS);

### From source

```sh
sudo su
mkdir -p /epics/iocs/tools
cd /epics/iocs/tools/
git clone https://github.com/douglasbeniz/iocServicesMonitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Here it is necessary to configure the service to start the monitor. It could be running as 'main' (shows a list of configured servers) or as 'api' (monitor IOC services at current server);

1. edit iocServicesMonitor.py and change the variables as desired (could simple uncomment the lines there):
- iocServicesMonitor = create_app(register_main=True)
- iocServicesMonitor = create_app(register_api=True)
2. edit file ioc@services-monitor.service copied to /etc/systemd/system/; what should be updated:
- `ConditionHost`;
- <Server_IP> at `ExecStart`; port `5000` is being used as the default for this tool;
