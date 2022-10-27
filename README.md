# UFiber-Disabler

This is a project takes a mac address, logs into each OLT listed in a database (Which is created with setup.py) and dumps the MAC Table, searches those MAC Tables for the approprate MAC Address, then changes the VLAN to the one specified.

## Getting Started
### Dependencies
    pip install ipaddress
    pip install getpass

### Setup
Run setup.py to create the SQLite3 database which is where the IP, Username, and Passwords will be stored for all OLTs. Keep in mind that none of these fields are encrypted

## Usage
python3 main.py -m mac_address -v vlan [-o OLT...] [-h]
    
    Options:
        -m, --mac       (Required) Takes 1 MAC Address e.g. -m ff:ff:ff:ff:ff:ff
        -v, --vlan      Takes 1 VLAN ID to set as untagged on port 1 of the ONU e.g. -v 255
        -o, --olt       Takes 1 or more comma separated IPs for OLTs, IPs need to already have an entry in the database
        -h, --help      Prints the Help menu
