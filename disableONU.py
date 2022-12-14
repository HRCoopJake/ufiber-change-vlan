import requests
import json
from urllib3.exceptions import InsecureRequestWarning

def getONUSettings(baseurl, token, serialNum):
    url = f"{baseurl}gpon/onus/{serialNum}/settings"
    HEADER = {'x-auth-token': token}

    response = requests.get(verify=False, url=url, headers=HEADER)

    return json.loads(response.content)

def disableONU(baseurl, token, serialNum, settings, newVLAN):
    settings['bridgeMode']['ports'][0]['nativeVLAN'] = int(newVLAN)
    url = f"{baseurl}gpon/onus/{serialNum}/settings"
    HEADER = {'x-auth-token': token}

    response = requests.put(verify=False, url=url, headers=HEADER, data=str(settings))
    if response.status_code == 200:
        print("Success!")
    else:
        print("Recieved HTTP Code {}".format(response.status_code))