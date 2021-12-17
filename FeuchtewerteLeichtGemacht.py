import json
from Runner import refreshT
from openpyxl import Workbook,load_workbook
import requests
from NavigateInExcel import searchXL
from datetime import datetime
import time
def OnlyUsableDestinations(data):
    obj = data.json()
    CPlist = []
    for elements in obj['content']:
        if str(elements['uniqueId'])[13:15] == "CP" and int(elements['masterData']['chargingFacilities'][0]['power']) < 350 and str(elements['firmwareVersion']) != "" and int(elements['masterData']['chargingFacilities'][0]['power']) > 150:
            CPlist.append(elements)

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
    FeuchteTbl = wb.worksheets[0]
    FeedbackTbl = wb.worksheets[1]

    #obj = data.json()

    searchTerm = "Feuchte " + datetime.today().strftime('%d.%m.%Y')
    TodayCol = searchXL(FeuchteTbl, searchTerm)[1]

    j = 1
    CPlist = []
    for elements in obj:
        if str(elements['uniqueId'])[13:18] == "CPN01":
            url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01/request?lmsGlobalId=0000000000000005010f&force=true"
            update_message = BackendRequestTemplate(atoken, url, s)
            print(str(elements['uniqueId'])[13:18] + " i=" + str(j))
            CPlist.append(elements)
            j= j +1
    i = 1
    for elements in CPlist:
        print(str(elements['uniqueId'])[13:18])
        url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + str(elements['uniqueId'])[:13] + "LMS01?lmsGlobalId=00000000000e0005010f"
        measurement = BackendRequestTemplate(atoken, url, s)
        measurementJ = measurement.json()
        content = measurementJ['message']
        if content == None:
            humidity = 255
        else:
            if content['idents'][14]['value'] == "Closed" or content['idents'][14]['value'] == "":
                #print(content['idents'][14]['value'])
                humidity = 999
            else:
                #print(content['idents'][14]['value'])
                humidity = content['idents'][14]['value']

#searchID and fill in humidity
        Xcp = searchXL(FeuchteTbl, str(elements['uniqueId']))
        if Xcp != "notFound":
            FeuchteTbl.cell(row=Xcp[0], column=TodayCol).value = int(humidity)
            FeedbackMessage = "Found in row: " + str(Xcp)
        else:
            FeedbackMessage = "Not found"

        print(humidity)
        FeedbackTbl.cell(row=i, column=1).value = str(elements['uniqueId'])[:2]
        FeedbackTbl.cell(row=i, column=2).value = str(elements['masterData']['chargingFacilities'][0]['power'])
        FeedbackTbl.cell(row=i, column=3).value = str(elements['uniqueId'])
        FeedbackTbl.cell(row=i, column=4).value = str(elements['masterData']['chargePointName'])
        FeedbackTbl.cell(row=i, column=5).value = str(elements['firmwareVersion'])
        FeedbackTbl.cell(row=i, column=6).value = str(elements['uniqueId'])[13:]
        FeedbackTbl.cell(row=i, column=7).value = int(humidity)
        FeedbackTbl.cell(row=i, column=8).value = FeedbackMessage
        i = i+1

    wb.save('PythonZuExcel.xlsx')

if __name__ == "__main__":
    i = 0
    #url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=1000&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=ACTIVE&status=FAULTED&status=INACTIVE"
    url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=1000&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC"
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