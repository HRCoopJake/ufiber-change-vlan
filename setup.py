import sqlite3
from sqlite3 import Error
import ipaddress
import getpass


def sql_connection():
    conn = None

    try:
        conn = sqlite3.connect("database.db")
        return conn
    except Error as e:
        print(e)

def checkForTable(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='olts'")
    returned = cursor.fetchone()
    if not returned:
        print("Creating Table")
        cursor.execute("CREATE TABLE olts (ip TEXT, username TEXT, password TEXT)")
    else:
        print("Table already created with the following entries:")
        cursor.execute("SELECT ip,username FROM olts")
        olt = cursor.fetchall()
        print("IP Address, Username")
        for i in olt:
            print(i)


connection = sql_connection()
cursor = connection.cursor()
checkForTable(cursor)
connection.commit()

print("\nEnter OLT information\nType 'done' when all olts have been put in")
while True:
    ip = input('\nIP Address: ')
    if ip == 'done':
        break
    
    try:
        ipaddress.ip_network(ip)
    except:
        print(f"{ip} is not an IP Address")
        continue
    
    username = input('Username: ')
    if username == '':
        print("Username was empty. Try again")
        continue

    password = getpass.getpass('Password: ')
    if password == '':
        print("Password was empty. Try again")
        continue
    
    cursor.execute(f"INSERT INTO olts (ip,username,password) VALUES ('{ip}','{username}','{password}')")
    connection.commit()
