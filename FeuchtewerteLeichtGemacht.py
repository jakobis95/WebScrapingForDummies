import json
from Runner import refreshT
from openpyxl import Workbook,load_workbook
import requests
import time
def OnlyUsableDestinations(data):
    obj = data.json()
    uniqueIdlcp = "empty"
    CPlist = []
    for elements in obj['content']:
        if str(elements['uniqueId'])[13:15] == "CP" and int(elements['masterData']['chargingFacilities'][0]['power']) < 350 and str(elements['firmwareVersion']) != "":
            if not str(elements['uniqueId'])[:13] == uniqueIdlcp[:13]:
                CPlist.append(elements)
                #url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01/request?lmsGlobalId=0000000000000005010f&force=true"
                #update_message = BackendRequestTemplate(atoken, url, s)
                #j = j + 1
                #print(update_message.text + " : " + str(j) + "/220")
                #time.sleep(1)
        uniqueIdlcp = str(elements['uniqueId'])

    for elements in CPlist:
        print(elements['uniqueId'][:13])

    return CPlist
def BackendRequestTemplate(atoken, url, s):
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
    #print(p)
    #print("return P.TEXT")
    return p

def auswertungBackenddaten(obj, atoken, s):
    uniqueIdlcp = ""
    humidity = "999"
    print("Auswertung")
    i = 1
    wb = load_workbook(filename='PythonZuExcel.xlsx')
    Tabellenblatt = wb.active
    #obj = data.json()
    j = 0
    CPlist = []
    for elements in obj:
        url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01/request?lmsGlobalId=0000000000000005010f&force=true"
        update_message = BackendRequestTemplate(atoken, url, s)
        #time.sleep(1)
    print("alle standorte:::::::::")
    for elements in obj:
        if str(elements['uniqueId'])[13:15] == "CP" and int(elements['masterData']['chargingFacilities'][0]['power']) < 350 and str(elements['firmwareVersion']) != "":
            if str(elements['uniqueId'])[:12] == uniqueIdlcp[:12]:
                Tabellenblatt.cell(row=i-1, column=6).value = "CPN012"
            else:
                #print("https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01?lmsGlobalId=00000000000e0005010f")
                url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01?lmsGlobalId=00000000000e0005010f"
                measurement = BackendRequestTemplate(atoken, url, s)
                measurementJ = measurement.json()
                content = measurementJ['message']
                if content == None:
                    humidity = 255
                else:

                    if content['idents'][14]['value'] == "Closed" or content['idents'][14]['value'] == "":
                        print(content['idents'][14]['value'])
                        humidity = 999
                    else:
                        print(content['idents'][14]['value'])
                        humidity = content['idents'][14]['value']



                #print(humidity)
                CPlist.append(str(elements['masterData']['chargingFacilities'][0]['power']) + ":" + str(elements['uniqueId']) + ":" + str(elements['masterData']['chargePointName']) + " : " + str(elements['firmwareVersion']) + " : " + str(humidity) )
                Tabellenblatt.cell(row=i, column=1+8).value = str(elements['uniqueId'])[:2]
                Tabellenblatt.cell(row=i, column=2+8).value = str(elements['masterData']['chargingFacilities'][0]['power'])
                Tabellenblatt.cell(row=i, column=3+8).value = str(elements['uniqueId'])
                Tabellenblatt.cell(row=i, column=4+8).value = str(elements['masterData']['chargePointName'])
                Tabellenblatt.cell(row=i, column=5+8).value = str(elements['firmwareVersion'])
                Tabellenblatt.cell(row=i, column=6+8).value = str(elements['uniqueId'])[13:]
                Tabellenblatt.cell(row=i, column=7+8).value = int(humidity)


    wb.save('PythonZuExcel.xlsx')

if __name__ == "__main__":
    i = 0
    url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=1000&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=ACTIVE&status=FAULTED&status=INACTIVE"

    s = requests.session()
    refreshT(s)
    with open('token2.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print("vergleich")
        print(data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    data = BackendRequestTemplate(atoken, url, s)
    data = OnlyUsableDestinations(data)
    auswertungBackenddaten(data, atoken, s)