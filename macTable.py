import requests
import json

def getONUs(baseurl, token):
    url = f"{baseurl}tools/mac-table"

    HEADER = {'x-auth-token': token}

    response = requests.get(
        verify=False,
        url=url,
        headers=HEADER
    )
    return json.loads(response.content)

def findMAC(onus, mac):
    returned_onus = []
    for i in onus:
        if i['mac'].lower() == mac.lower():
            returned_onus.append(i['onu'])
    return returned_onus