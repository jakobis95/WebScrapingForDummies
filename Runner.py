#from bs4 import BeautifulSoup
import requests
import json
import time
from SessionPPN_call import refreshT


import certifi #brauche ich gerade wohl nicht
import urllib3 #brauche ich gerade wohl nicht

def RequestCopy(atoken, url, s):
    http = urllib3.PoolManager()


    #url = 'https://api.chargepoint-management.com/maintenance/v1/measurements/ES9110000135_LMS01?lmsGlobalId=00000000000e0005010f'
    headers = {
        'authority': 'api.chargepoint-management.com',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://www.chargepoint-management.com',
        'Referer': 'https://www.chargepoint-management.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Authorization': atoken
    }

    p = s.get(url, headers=headers,  verify=False)
    print(p)
    with open('Info.json', 'w') as f:
        f.write(p.text)
    with open('Info.json', 'r' ) as c:
        obj = json.load(c)
        print(obj['content'])
        for elements in obj['content']:
            if elements['power'] == 320:
                print(elements['uniqueId'] + ":" + elements['chargingFacilities']['power'])
    # r = http.request('GET', 'https://api.chargepoint-management.com/status/connectionStatusList', headers=headers)
    # print(r.headers)
    # print(json.loads(r.data))
if __name__ == '__main__':
    list = ["https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=100&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED"
            ]
    s = requests.session()
    refreshT(s)
    with open('token2.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print("vergleich")
        print( data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    for url in list:
        print(url)
        RequestCopy(atoken,url,s)
        #time.sleep(1)