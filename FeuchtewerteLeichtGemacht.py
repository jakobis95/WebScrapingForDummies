import json
from Runner import refreshT
import requests

def BackendRequestTemplate(atoken, url, s, i):
    #http = urllib3.PoolManager()


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
    Zustand = ["fehler.json", "offline.json", "alle.json"]
    with open(Zustand[i], 'w') as f:
        f.write(p.text)
    with open(Zustand[i], 'r' ) as c:
        obj = json.load(c)
        print(Zustand[i] + ":::::::::")
        for elements in obj['content']:
            if str(elements['uniqueId'])[13:15] == "CP" and int(elements['masterData']['chargingFacilities'][0]['power']) < 350 and str(elements['firmwareVersion']) != "":
                print(str(elements['masterData']['chargingFacilities'][0]['power']) + ":" + str(elements['uniqueId']) + ":" + str(elements['masterData']['chargePointName']) + " : " + str(elements['firmwareVersion']))

    # r = http.request('GET', 'https://api.chargepoint-management.com/status/connectionStatusList', headers=headers)
    # print(r.headers)
    # print(json.loads(r.data))

if __name__ == "__main__":
