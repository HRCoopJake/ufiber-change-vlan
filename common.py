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

Usage: python3 main.py -m mac_address [-o OLT...] [-h]
    
    Options:
        -m, --mac       (Required) Takes 1 MAC Address e.g. -m ff:ff:ff:ff:ff:ff
        -o, --olt       Takes 1 or more comma separated IPs for OLTs
        -h, --help      Prints this menu
        """
    )
    sys.exit()

def parseArgs():
    defaultThings = defaultSettings()

    usage = """This program moves a single Ubiquiti ONU to a new VLAN

Usage: python3 main.py -m mac_address [-o OLT...] [-h]
    
    Options:
        -m, --mac       (Required) Takes 1 MAC Address e.g. -m ff:ff:ff:ff:ff:ff
        -o, --olt       Takes 1 or more comma separated IPs for OLTs
        -h, --help      Prints this menu
    """
    
    p = argparse.ArgumentParser(prog='main',
                                usage=usage,
                                description="This program moves a single Ubiquiti ONU to a new VLAN",
                                argument_default=argparse.SUPPRESS) # Don't overwrite attributes with None
    
    p.add_argument('-o', '--olt', dest='olts', help='List of OLTs')
    p.add_argument('-m', '--mac', dest='mac', help='MAC Address to look for')

    default_settings = defaultSettings
    args = p.parse_args(namespace=default_settings())
    
    if args.mac:
        defaultThings.mac = args.mac
    else:
        printHelp()
    
    if args.olts:
        olts = args.olts.split(",")
        defaultThings.olts = olts
    else:
        defaultThings.olts = olt()
    
    return defaultThings

def sql_connection():
    conn = None

    try:
        conn = sqlite3.connect("database.db")
        
        # Creates and commits the table if it isn't made yet
        conn.cursor().execute("CREATE TABLE IF NOT EXISTS olts (ip TEXT, username TEXT, password TEXT)")
        conn.commit()
        return conn
    except Error as e:
        print(e)

def olt():
    connection = sql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM olts")
    oltList = cursor.fetchall()
    return oltList

class defaultSettings:
    mac = ''
    olts = []
