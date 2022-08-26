
import json
import os
import time
import requests
from A1_Working_Skripts.A2_Status_To_XL import WriteStatusToXL
from A1_Working_Skripts.A4_Jira_Bugs_to_XL import write_Bugs_to_XL
from A1_Working_Skripts.A3_VR16_HVAC_To_XL import start_Update_from_Jira
from A1_Working_Skripts.A1_Update_Status_from_CPM import BackendRequestTemplate,cpstate,authLoopRequest
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from A2_Working_Support_Functions.FileManagementTools import  check_files_timeliness
from A1_Working_Skripts.A5_Jira_Epic_Abgleich import isEpicLocationMatched

def updateLocations(tokenPath, offlinestandorteTxtPath,fehlerstandorteTxtPath, JSONSamplePath):
    # CBXStatusUpdate
    urllist = [
        "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED",
        "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
    ]

    # askForToken()
    s = requests.session()
    authLoopRequest(s, tokenPath)
    with open(tokenPath, 'r') as jsonf:
        data = json.load(jsonf)
        print(data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    UserName = os.getlogin()
    i = 0
    fehlerstandorte = BackendRequestTemplate(atoken, urllist[0], s, i)  # typ = fehler
    i = 1
    # get_error_msg(fehlerstandorte, atoken, s)
    offlinestandorte = BackendRequestTemplate(atoken, urllist[1], s, i)  # typ = offline
    f = open(offlinestandorteTxtPath, 'w')
    f.write(json.dumps(offlinestandorte))
    authLoopRequest(s, tokenPath)

    with open(tokenPath, 'r') as jsonf:
        data = json.load(jsonf)
        print(data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    print("cpstate starting")
    fehlerstandorteStatus = cpstate(fehlerstandorte, atoken, s, JSONSamplePath)
    print("cpstate finished")
    f = open(fehlerstandorteTxtPath, 'w')
    f.write(json.dumps(fehlerstandorteStatus))

def fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, master_xlsx_path):
    # FillCbxStatusPAG
    print("load Json")
    f = open(
        fehlerstandorteTxtPath,
        'r')
    fehlerCBX = json.load(f)
    f = open(
        offlinestandorteTxtPath,
        'r')
    offlineCBX = json.load(f)
    print("WriteStatusToXL starting")
    WriteStatusToXL(master_xlsx_path, offlineCBX, fehlerCBX)
    time.sleep(1)

def updateVR16_HVAC(jira_xlsx_path_HVAC, jira_xlsx_path_VR16, master_xlsx_path):
    # Update_VR16_HVAC_xl
    print("\nstart_Update_from_Jira starting")
    start_Update_from_Jira(jira_xlsx_path_HVAC, jira_xlsx_path_VR16, master_xlsx_path)
    time.sleep(1)

def updateCurrentBugs(jira_CSV_Path, master_xlsx_path):
    # Jira_Bugs_to_XL
    write_Bugs_to_XL(jira_CSV_Path, master_xlsx_path)
    time.sleep(1)

def jiraEpicAbgleich(Master_XLSX_Path, destination_XLSX_Path):
    isEpicLocationMatched(Master_XLSX_Path,destination_XLSX_Path)

if __name__ == "__main__":

#Data directory
    input("Wurde eine Spalte für den heutigen Tag angelegt? Bitte mit Enter bestätigen.")
    input("Stellen Sie sicher dass Sie nicht im Porsche Wlan/Netzwerk sind? Bitte mit Enter bestätigen.")
    disable_warnings(InsecureRequestWarning)
    UserName = os.getlogin()
    jira_xlsx_path_HVAC = "C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx"
    jira_xlsx_path_VR16 = "C:\\Users\\" + str(UserName) + "\\Downloads\\VR16UpdatedStations.xlsx"
    master_xlsx_path = "C:\\Users\\" + str(UserName) + "\\Downloads\\IBN_Tracking.xlsx"
    jira_CSV_Path = "C:\\Users\\" + str(UserName) + "\\Downloads\\current_bugs.xlsx"

    files = [jira_xlsx_path_VR16, jira_xlsx_path_HVAC, jira_CSV_Path]
    if check_files_timeliness(files) != True:
        print("Ihre Jira Dateien sind nicht aktuell und ihr skript wurde beendet")
        exit()
#CBXStatusUpdate
    tokenPath = 'C:/Users/AJ2MSGR/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/refreshtoken.txt'
    urllist = ["https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED",
            "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
            ]

    #askForToken(tokenPath)
    s = requests.session()
    authLoopRequest(s, tokenPath)
    with open(tokenPath, 'r') as jsonf:
        data = json.load(jsonf)
        print( data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    i = 0
    fehlerstandorte = BackendRequestTemplate(atoken,urllist[0],s,i) #typ = fehler
    i = 1
    #get_error_msg(fehlerstandorte, atoken, s)
    offlinestandorte = BackendRequestTemplate(atoken, urllist[1], s, i ) #typ = offline
    offlinestandorteTxtPath = "C:/Users/"+ UserName+"/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/offlinestandorte.text"
    f = open(offlinestandorteTxtPath, 'w')
    f.write(json.dumps(offlinestandorte))
    authLoopRequest(s, tokenPath)

    with open(tokenPath, 'r') as jsonf:
         data = json.load(jsonf)
         print(data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    fehlerstandorteTxtPath = "C:/Users/"+ UserName+"/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text"
    JSONSamplePath = "C:/Users/" + UserName + "/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/JSONsample.txt"
    print("cpstate starting")
    fehlerstandorteStatus = cpstate(fehlerstandorte, atoken, s, JSONSamplePath)
    print("cpstate finished")
    f = open("C:/Users/"+ UserName+"/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text", 'w')
    f.write(json.dumps(fehlerstandorteStatus))

#FillCbxStatusPAG
    print("load Json")
    f = open("C:/Users/"+ UserName+"/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text", 'r')
    fehlerCBX = json.load(f)
    f = open("C:/Users/"+ UserName+"/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/offlinestandorte.text", 'r')
    offlineCBX = json.load(f)
    print("WriteStatusToXL starting")
    WriteStatusToXL(master_xlsx_path, offlineCBX, fehlerCBX)
    time.sleep(5)

#Update_VR16_HVAC_xl
    print("start_Update_from_Jira starting")
    start_Update_from_Jira(jira_xlsx_path_HVAC,jira_xlsx_path_VR16,master_xlsx_path)
    time.sleep(5)

#Jira_Bugs_to_XL
    write_Bugs_to_XL(jira_CSV_Path, master_xlsx_path)
    time.sleep(5)

#Finished Prozess open complete file
    os.startfile(master_xlsx_path)

