import json
import os
from A2WorkingSkrips.CBXStatusUpdate import authLoopRequest
import requests
from FeuchtewerteLeichtGemacht import BackendRequestTemplate, OnlyUsableDestinations
import pandas as pd
def cutId(id):
    return id[:12]

def updateMeasurement(uniqueId, atoken, s, type):#type ("3"=LK, "5"=CBC)
    url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + uniqueId[:13] + "LMS01/request?lmsGlobalId=000000000000000"+type+"0"+ uniqueId[-1] +"0f&force=true"
    updateMessage = BackendRequestTemplate(atoken, url, s)
    return updateMessage

def getMeasurement(uniqueId, atoken, s, type):#type ("3"=LK, "5"=CBC)
    url = "https://api.chargepoint-management.com/maintenance/v1/measurements/" + uniqueId[:13] + "LMS01?lmsGlobalId="+ uniqueId[0:2].lower() + uniqueId[2:] +"000e000"+ type +"0"+ uniqueId[-1]+"0f"
    measurement = BackendRequestTemplate(atoken, url, s)
    measurementJ = measurement.json()
    return measurementJ


if __name__ == "__main__":
    i = 0
    url = "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=1000&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC"
    s = requests.session()
    UserName = os.getlogin()
    authLoopRequest(s)
##########
    Basis = '''{
        "Standorte": [

        ]
    }'''
    Standort = '''
    {
        "ID": "234234",
        "Subsysteme":{}
    }
    '''
    Subsysteme = '''
    {
        "LKs": {},
        "CBCs":{}
    }
    '''
    LKmeas = '''
    {
        "LK1": {},
        "LK2": {}
    }
    '''
    CBCmeas = '''
        {
            "CBC1": {},
            "CBC2": {}
        }
        '''
    jBasis = json.loads(Basis)
    jStandort = json.loads(Standort)
    jSubsystem = json.loads(Subsysteme)
    jLKmeas = json.loads(LKmeas)
    jCBCmeas = json.loads(CBCmeas)

    with open('DataFiles/refreshtoken.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print("vergleich")
        print(data['refresh_token'])

    atoken = 'Bearer ' + data['access_token']
    data = BackendRequestTemplate(atoken, url, s)
    data = OnlyUsableDestinations(data)
    f = open("DataFiles/UsableDestinationsDaily.txt", 'w')
    f.write(json.dumps(data))
    df = pd.DataFrame(data)
    df["group"] = df["uniqueId"].apply(cutId)
    df = df.loc[:,["uniqueId","group"]]
    #df = df.iloc[10]
    grouped = df.groupby("group")
    #grouped = grouped.iloc[:, 0:5]



    #for i in range(0,10):
    #    print(i)
    #    print(updateMeasurement(str(data[i]['uniqueId']), atoken, s, "5"))
    #    print(updateMeasurement(str(data[i]['uniqueId']), atoken, s, "3"))
    j = 0
    for i in data:
        print(updateMeasurement(str(i['uniqueId']), atoken, s, "5"))
        print(updateMeasurement(str(i['uniqueId']), atoken, s, "3"))
        print(j)
        j = j + 1
        if j % 100 == 0:
            authLoopRequest(s)
            with open('DataFiles/refreshtoken.txt', 'r') as jsonf:
                token = json.load(jsonf)
            atoken = 'Bearer ' + token['access_token']
    i = 0
    for name, group in grouped:
        id = group.iat[0, 1]
        print(id[0:12])
        jBasis["Standorte"].append(jStandort)
        jBasis["Standorte"][i]["Subsysteme"] = jSubsystem
        jBasis["Standorte"][i]["Subsysteme"]["LKs"] = jLKmeas
        jBasis["Standorte"][i]["Subsysteme"]["CBCs"] = jCBCmeas
        jBasis["Standorte"][i]["ID"] = name
        fileSave = json.dumps(jBasis, indent=2)
        jBasis = json.loads(fileSave)
        for id in group["uniqueId"]:
            CBCdata = getMeasurement(str(id), atoken, s, "5")

            jBasis["Standorte"][i]["Subsysteme"]["CBCs"]["CBC" + str(id[-1])] = CBCdata
            print(i)
            LKdata = getMeasurement(str(data[i]['uniqueId']), atoken, s, "3")
            jBasis["Standorte"][i]["Subsysteme"]["LKs"]["LK" + str(id[-1])] = LKdata
            fileSave = json.dumps(jBasis, indent=2)
            jBasis = json.loads(fileSave)
        i = i + 1
        if i % 100 == 0:
            authLoopRequest(s)
            with open('DataFiles/refreshtoken.txt', 'r') as jsonf:
                token = json.load(jsonf)
            atoken = 'Bearer ' + token['access_token']
        #if i >= 10:
         #   break
    print(json.dumps(jBasis, indent=2))
    with open("C:\\Users\\AJ2MSGR\\Documents\\CBXmeasurements2.json", "w") as doc:
        json.dump(jBasis, doc, indent=2)