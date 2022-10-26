import requests
from urllib3.exceptions import InsecureRequestWarning
import sys

from macTable import getONUs, findMAC
from common import getToken,parseArgs,defaultSettings
from disableONU import getONUSettings, disableONU

# Supresses SSL certificate errors
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

args = parseArgs()

serialNumbers = []
for i in args.olts:
    baseurl = f'https://{i[0]}/api/v1.0/'
    token = getToken(baseurl,i[1],i[2])
    onus = getONUs(baseurl, token)
    serialNUMlist = findMAC(onus, args.mac)

    if len(serialNUMlist) == 1:
        serialNUM = serialNUMlist[0]
    else:
        print(f"Error!! There were {len(serialNUMlist)} ONUs found in my search")
        sys.exit()

settings = getONUSettings(baseurl, token, serialNUM)
disableONU(baseurl, token, serialNUM, settings,144)