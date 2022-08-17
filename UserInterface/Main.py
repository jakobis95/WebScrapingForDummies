from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import os
import time
import requests
import A3SupportingGeneralFunctions.FileManagementTools as fileMan
from pagAutoStatus.FillCbxStatusPAG import WriteStatusToXL
from pagAutoStatus.Jira_Bugs_to_XL import write_Bugs_to_XL
from pagAutoStatus.Update_VR16_HVAC_xl import start_Update_from_Jira
from A2WorkingSkrips.CBXStatusUpdate import BackendRequestTemplate,cpstate,authLoopRequest,get_error_msg
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings


def check_files_timeliness(files):
    uptodate = True
    for file in files:
        if fileMan.is_uptodate(file):
            print("uptodate\n ->>", file)
        else:
            print("NOT UPTODATE\n ->>", file)
            uptodate = False

    if uptodate == False:
        print("Outdated File detected!!!, you want to continue anyway?")
        decision = False
        while decision != True:
            response = input("Press y to continue or n to terminate programm")
            if response == "y":
                decision = True
                return True
            if response == "n":
                decision = True
                return False
    else:
        return True
def askForToken():
    tokentxt = input("Bitte geben Sie einen aktuellen Authentifizierungstoken ein und bestätigen Sie mit Enter")
    with open(tokenPath, 'w') as f:
        f.write(tokentxt)
    f.close()


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

    #askForToken()
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

