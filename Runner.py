#from bs4 import BeautifulSoup
import requests
import json
import time
#from SessionPPN_call import refreshT


import certifi #brauche ich gerade wohl nicht
import urllib3 #brauche ich gerade wohl nicht


def cpstate(fehlerstandorte):
    Status = ""
    StatusListe = []
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
    for elements in fehlerstandorte:
        url = ("https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:12] + "_LMS01/request?lmsGlobalId=de911000016700030"+ str(elements['uniqueId'])[17] +"0a&force=true")
        s.get(url, headers=headers, verify=False)
        #time.sleep(1)

#fehlerstandorte durchgehen
    f = open("JSONsample.txt")
    JSONlist = json.load(f)

    for elements in fehlerstandorte:
        url = ("https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:12] + "_LMS01?lmsGlobalId=de911000016700030" +str(elements['uniqueId'])[17] + "0a")
        print(url)
        CPdata = s.get(url, headers=headers, verify=False)
        time.sleep(2)
        CPdataJ = CPdata.json()

        if CPdataJ['message'] == None:
            Status = "Error"
        else:
            Status = str(CPdataJ['message']['idents'][8]['value'])
        #print(str(elements['masterData']['chargePointName']) + " : " +str(elements['uniqueId']) + " : " + Status)
        StatusListe.append( Status + " : " + str(elements['masterData']['chargePointName']) + " : " +str(elements['uniqueId']))

        element = {"chargePointName": "", "uniqueId": "", "Status": ""}
        element['chargePointName'] = elements['masterData']['chargePointName']
        element['Status'] = Status
        element['uniqueId'] = elements['uniqueId']
        print(element)
        JSONlist.append(element)

    print(JSONlist)
    for content in StatusListe:
        print(content)
    return JSONlist

def BackendRequestTemplate(atoken, url, s, i):
    http = urllib3.PoolManager()
    CPList = []

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
    CPList = []
    Zustand = ["fehler.json", "offline.json", "alle.json"]
    with open(Zustand[i], 'w') as f:
        f.write(p.text)
    with open(Zustand[i], 'r' ) as c:
        obj = json.load(c)
        print(Zustand[i] + ":::::::::")
        for elements in obj['content']:
            if str(elements['uniqueId'])[13:15] == "CP"  and str(elements['firmwareVersion']) != "":
                if str(elements["manufacturerModelId"]["name"]) == "DC CBX":
                    print(str(elements['masterData']['chargingFacilities'][0]['power']) + ":" + str(elements['uniqueId']) + ":" + str(elements['masterData']['chargePointName']) + " : " + str(elements['firmwareVersion']))
                    CPList.append(elements)

    return CPList
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
    urllist = ["https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED",
            "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
            ]
    s = requests.session()
    refreshT(s)
    with open('token2.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print("vergleich")
        print( data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    i = 0
    fehlerstandorte = BackendRequestTemplate(atoken,urllist[0],s,i) #typ = fehler
    i = 1
    offlinestandorte = BackendRequestTemplate(atoken, urllist[1], s, i ) #typ = offline

    f = open("offlinestandorte.text", 'w')
    f.write(json.dumps(offlinestandorte))

    fehlerstandorteStatus = cpstate(fehlerstandorte)

    f = open("fehlerstandorteStatus.text", 'w')
    f.write(json.dumps(fehlerstandorteStatus))
