import argparse
import sys
import requests
import sqlite3
from sqlite3 import Error


def getToken(baseurl,username,password):
    url = f"{baseurl}user/login"
    form_data = {}
    form_data['username'] = username
    form_data['password'] = password
    form_data = str(form_data)

    HEADER = {}
    response = requests.post(
        verify=False,
        url=url,
        headers=HEADER,
        data=form_data
    )
    return response.headers['x-auth-token']

def printHelp():
    print(
        """This program moves a single Ubiquiti ONU to a new VLAN

Usage: python3 main.py -m mac_address -v vlan [-o OLT...] [-h]
    
    Options:
        -m, --mac       (Required) Takes 1 MAC Address e.g. -m ff:ff:ff:ff:ff:ff
        -v, --vlan      Takes 1 VLAN ID to set as untagged on port 1 of the ONU e.g. -v 255
        -o, --olt       Takes 1 or more comma separated IPs for OLTs
        -h, --help      Prints this menu
        """
    )
    sys.exit()

def parseArgs():
    defaultThings = defaultSettings()

    usage = """This program moves a single Ubiquiti ONU to a new VLAN

Usage: python3 main.py -m mac_address -v vlan [-o OLT...] [-h]
    
    Options:
        -m, --mac       (Required) Takes 1 MAC Address e.g. -m ff:ff:ff:ff:ff:ff
        -v, --vlan      Takes 1 VLAN ID to set as untagged on port 1 of the ONU e.g. -v 255
        -o, --olt       Takes 1 or more comma separated IPs for OLTs
        -h, --help      Prints this menu
    """
    
    p = argparse.ArgumentParser(prog='main',
                                usage=usage,
                                description="This program moves a single Ubiquiti ONU to a new VLAN",
                                argument_default=argparse.SUPPRESS) # Don't overwrite attributes with None
    
    p.add_argument('-o', '--olt', dest='olts', help='List of OLTs')
    p.add_argument('-m', '--mac', dest='mac', help='MAC Address to look for')
    p.add_argument('-v', '--vlan', dest='vlan', help='Which VLAN to set as untagged on Ethernet interface')

    default_settings = defaultSettings
    args = p.parse_args(namespace=default_settings())
    
    if args.mac:
        defaultThings.mac = args.mac
    else:
        printHelp()
    
    if args.vlan:
        defaultThings.vlan = args.vlan
    else:
        printHelp()

    if args.olts:
        olts = args.olts.split(",")
        if len(olts) == 1:
            oltsCreds = olt(f"('{olts[0]}')")
        else:
            oltsCreds = olt(tuple(olts))

        for i in oltsCreds:
            if i[0] in olts:
                index = olts.index(i[0])
                olts.pop(index)
        if olts:
            print(f"{olts} aren't in database")
            sys.exit()

        defaultThings.olts = oltsCreds
    else:
        defaultThings.olts = olt(False)
    
    return defaultThings

def sql_connection():
    conn = None

    try:
        return sqlite3.connect("database.db")
    except Error as e:
        print(e)

def olt(fromTuple):
    connection = sql_connection()
    cursor = connection.cursor()

    if not fromTuple:
        cursor.execute("SELECT * FROM olts")
        oltList = cursor.fetchall()
        return oltList
    else:
        cursor.execute(f"SELECT * FROM olts WHERE ip IN {fromTuple}")
        return cursor.fetchall()

class defaultSettings:
    mac = ''
    olts = []
    vlan = ''
