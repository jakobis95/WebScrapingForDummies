from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import os
import requests
from pagAutoStatus.FillCbxStatusPAG import WriteStatusToXL
from pagAutoStatus.Jira_Bugs_to_XL import write_Bugs_to_XL
from pagAutoStatus.Update_VR16_HVAC_xl import start_Update_from_Jira
from A2WorkingSkrips.CBXStatusUpdate import BackendRequestTemplate,cpstate,authLoopRequest,get_error_msg

def get_File_property():
    from pathlib import *
    p = Path("C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx")
    pct = p.stat().st_mtime
    from datetime import datetime
    print(datetime.utcfromtimestamp(pct).strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":

#Data directory
    UserName = os.getlogin()
    jira_xlsx_path_HVAC = "C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx"
    jira_xlsx_path_VR16 = "C:\\Users\\" + str(UserName) + "\\Downloads\\VR16UpdatedStations.xlsx"
    master_xlsx_path = "C:\\Users\\" + str(UserName) + "\\Downloads\\IBN_Tracking.xlsx"
    jira_CSV_Path = "C:\\Users\\" + str(UserName) + "\\Downloads\\current_bugs.xlsx"

#CBXStatusUpdate
    i = 0
    urllist = ["https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=FAULTED",
            "https://api.chargepoint-management.com/chargepoint/chargepoints/list?page=0&size=500&sort=masterData.chargePointName,asc&masterData.chargingFacilities.powerType=DC&status=INACTIVE"
            ]
    s = requests.session()
    authLoopRequest(s)
    with open('DataFiles/refreshtoken.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print( data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    i = 0
    fehlerstandorte = BackendRequestTemplate(atoken,urllist[0],s,i) #typ = fehler
    i = 1
    get_error_msg(fehlerstandorte)
    offlinestandorte = BackendRequestTemplate(atoken, urllist[1], s, i ) #typ = offline
    f = open("DataFiles/offlinestandorte.text", 'w')
    f.write(json.dumps(offlinestandorte))
    authLoopRequest(s)
    with open('DataFiles/refreshtoken.txt', 'r') as jsonf:
        data = json.load(jsonf)
        print(data['refresh_token'])
    atoken = 'Bearer ' + data['access_token']
    fehlerstandorteStatus = cpstate(fehlerstandorte)
    f = open("DataFiles/fehlerstandorteStatus.text", 'w')
    f.write(json.dumps(fehlerstandorteStatus))

#FillCbxStatusPAG

    f = open("C:/Users/AJ2MSGR/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text", 'r')
    fehlerCBX = json.load(f)
    f = open("C:/Users/AJ2MSGR/PycharmProjects/WebScrapingForDummies/A2WorkingSkrips/DataFiles/offlinestandorte.text", 'r')
    offlineCBX = json.load(f)
    WriteStatusToXL(master_xlsx_path, offlineCBX, fehlerCBX)

#Update_VR16_HVAC_xl
    start_Update_from_Jira(jira_xlsx_path_HVAC,jira_xlsx_path_VR16,master_xlsx_path)

#Jira_Bugs_to_XL
    write_Bugs_to_XL(jira_CSV_Path, master_xlsx_path)

#Finished Prozess open complete file
    os.startfile(master_xlsx_path)

