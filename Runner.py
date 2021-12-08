#from bs4 import BeautifulSoup
import requests
import json
import time
#from SessionPPN_call import refreshT


import certifi #brauche ich gerade wohl nicht
import urllib3 #brauche ich gerade wohl nicht
# class urlHandler(object):
#     def __init__(self):
#         intern = intern
#     def LS1_Measurement(self, ID):
#         url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + ID + "?lmsGlobalId=00000000000e0003010a"
#         return url
#     def LS2_Measurement(self, ID):
#         url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + ID + "?lmsGlobalId=00000000000e0003020a"
#         return url
#     def CB_Measurement(self, ID):
#         url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + ID + "?lmsGlobalId=00000000000e0005010f"
#         return url
#     def inactive_Chargepoints(self):
#         url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
#         return url
#     def faulted_Chargepoints(self):
#         url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED"
#         return url
#     def all_DC_Chargepoints(self):
#         url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=ACTIVE&status=FAULTED&status=INACTIVE"
#         return url

def BackendRequestTemplate(atoken, url, s, i):
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

def refreshT(s): # Hier wird der Token refreshed
    #die verwendete Json datei wird aus dem Browser kopiert
    with open('refreshtoken.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print(data['refresh_token'])


    url = 'https://login.chargepoint-management.com/auth/realms/PAG/protocol/openid-connect/token'
    headers = {
        'authority' : 'api.chargepoint-management.com',
        'accept' : '*/*',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin' : 'https://www.chargepoint-management.com',
        'Referer':'https://www.chargepoint-management.com/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'AUTH_SESSION_ID=a4f12be7-2104-43c3-85a5-b62176eb82e3.e3b7f9c6-acc3-4abe-7b3a-4903; AUTH_SESSION_ID_LEGACY=a4f12be7-2104-43c3-85a5-b62176eb82e3.e3b7f9c6-acc3-4abe-7b3a-4903; KEYCLOAK_SESSION=PAG/12ca747b-237d-433c-afcc-9757ffe96d14/a4f12be7-2104-43c3-85a5-b62176eb82e3; KEYCLOAK_SESSION_LEGACY=PAG/12ca747b-237d-433c-afcc-9757ffe96d14/a4f12be7-2104-43c3-85a5-b62176eb82e3; KEYCLOAK_IDENTITY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiODJmYzRkZC1iOGI5LTQyODQtYjZlNy0wMTg3NTRlYWFiMzAifQ.eyJleHAiOjE2Mzg4NDgyNTEsImlhdCI6MTYzODgxMjI1MSwianRpIjoiZGFiYzMyYmQtYjJlOS00Njg2LWJkOTQtMGE3YWVmNDY0YmIyIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5jaGFyZ2Vwb2ludC1tYW5hZ2VtZW50LmNvbS9hdXRoL3JlYWxtcy9QQUciLCJzdWIiOiIxMmNhNzQ3Yi0yMzdkLTQzM2MtYWZjYy05NzU3ZmZlOTZkMTQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6ImE0ZjEyYmU3LTIxMDQtNDNjMy04NWE1LWI2MjE3NmViODJlMyIsInN0YXRlX2NoZWNrZXIiOiJ4bWNfcHdCMVFobThOczNQSkFrNW91cDROeFlTUmN2UUhkWnh4LVFzWFFRIn0.fcif5iM_sOKPwJEoIQ3lYFsKvP0p_i8MASjq_q09FEA; KEYCLOAK_IDENTITY_LEGACY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiODJmYzRkZC1iOGI5LTQyODQtYjZlNy0wMTg3NTRlYWFiMzAifQ.eyJleHAiOjE2Mzg4NDgyNTEsImlhdCI6MTYzODgxMjI1MSwianRpIjoiZGFiYzMyYmQtYjJlOS00Njg2LWJkOTQtMGE3YWVmNDY0YmIyIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5jaGFyZ2Vwb2ludC1tYW5hZ2VtZW50LmNvbS9hdXRoL3JlYWxtcy9QQUciLCJzdWIiOiIxMmNhNzQ3Yi0yMzdkLTQzM2MtYWZjYy05NzU3ZmZlOTZkMTQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6ImE0ZjEyYmU3LTIxMDQtNDNjMy04NWE1LWI2MjE3NmViODJlMyIsInN0YXRlX2NoZWNrZXIiOiJ4bWNfcHdCMVFobThOczNQSkFrNW91cDROeFlTUmN2UUhkWnh4LVFzWFFRIn0.fcif5iM_sOKPwJEoIQ3lYFsKvP0p_i8MASjq_q09FEA'
        }
    payload ={
        'grant_type':'refresh_token',
        'refresh_token' : data["refresh_token"],
        'client_id' : 'cpoc-frontend'
        }


    p = s.post(url, headers=headers, verify=False, data = payload )
    print(p)
    with open('token2.txt', 'w') as f:
        f.write(p.text)

    # with open('token2.txt', 'r') as jsonf:
    #     data = json.load(jsonf)
    #     print("vergleich")
    #     print( data['refresh_token'])
    #     print('Bearer ' + data['access_token'])

if __name__ == '__main__':
    i = 0
    list = ["https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED",
            "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
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
        BackendRequestTemplate(atoken,url,s,i)
        i = i+1