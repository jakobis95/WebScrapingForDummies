#from bs4 import BeautifulSoup
import requests
import json
from SessionPPN_call import refreshT


import certifi #brauche ich gerade wohl nicht
import urllib3 #brauche ich gerade wohl nicht

def RequestCopy(atoken, url):
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

    p = requests.get(url, headers=headers,  verify=False)
    print(p)
    with open('Info.txt', 'w') as f:
        f.write(p.text)

    # r = http.request('GET', 'https://api.chargepoint-management.com/status/connectionStatusList', headers=headers)
    # print(r.headers)
    # print(json.loads(r.data))
if __name__ == '__main__':
    list = ["https://api.chargepoint-management.com/maintenance/v1/measurements/DE9110000167_LMS01?lmsGlobalId=de91100001670001010f",
            "https://api.chargepoint-management.com/maintenance/v1/measurements/DE9110000168_LMS01?lmsGlobalId=de91100001670001010f",
            "https://api.chargepoint-management.com/maintenance/v1/measurements/DE9110000169_LMS01?lmsGlobalId=de91100001670001010f",
            "https://api.chargepoint-management.com/maintenance/v1/measurements/DE9110000170_LMS01?lmsGlobalId=de91100001670001010f"]
    s = requests.session()
    refreshT(s)
    with open('token2.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print("vergleich")
        print( data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    for url in list:
        print(url)
        RequestCopy(atoken,url)