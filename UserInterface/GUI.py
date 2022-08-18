import PySimpleGUI as sg
from pathlib import Path
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
from A3SupportingGeneralFunctions.FileManagementTools import askForToken, check_files_timeliness
# Path needed
disable_warnings(InsecureRequestWarning)
cwd = Path().cwd().parent
fehlerstandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text")
offlinestandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/offlinestandorte.text")
#Temp Programm parts
UserName = os.getlogin()
jira_xlsx_path_HVAC = "C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx"
jira_xlsx_path_VR16 = "C:\\Users\\" + str(UserName) + "\\Downloads\\VR16UpdatedStations.xlsx"
master_xlsx_path = "C:\\Users\\" + str(UserName) + "\\Downloads\\IBN_Tracking.xlsx"
jira_CSV_Path = "C:\\Users\\" + str(UserName) + "\\Downloads\\current_bugs.xlsx"

layout = [
    [sg.Text("CBX Doc Update Tool")],
    [sg.Multiline(size=(110, 10), echo_stdout_stderr=True, reroute_stdout=True, autoscroll=True,
                  background_color='black', text_color='white', key='-MLINE-')],
    [sg.Button("Run All")],
    [sg.Button("get Path")],
    [sg.Button("Excel mit CBX Status befüllen")]
    [sg.Button("Update Locations")],
    [sg.Button("Exit")]
]

# create the window
window = sg.Window("CDUT", layout)

# create an event loop
while True:
    event, values = window.read()
    # End prozess if user closes Window
    # presses the OK button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Run All":
        sg.popup("This Feature isnt currently implemented")
    if event == "get Path":
        cwd = Path().cwd().parent
        print(Path(cwd, "A2WorkingSkrips/DataFiles/refreshtoken.txt"))
    if event == "Excel mit CBX Status befüllen":
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
        time.sleep(5)

    if event == "Update Locations":
        # CBXStatusUpdate
        cwd = Path().cwd().parent
        print(Path(cwd, "A2WorkingSkrips/DataFiles/refreshtoken.txt"))
        tokenPath = Path(cwd, "A2WorkingSkrips/DataFiles/refreshtoken.txt")
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
        print(Path(cwd, "A2WorkingSkrips/DataFiles/offlinestandorte.text"))
        offlinestandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/offlinestandorte.text")
        f = open(offlinestandorteTxtPath, 'w')
        f.write(json.dumps(offlinestandorte))
        authLoopRequest(s, tokenPath)

        with open(tokenPath, 'r') as jsonf:
            data = json.load(jsonf)
            print(data['refresh_token'])
        atoken = 'Bearer ' + data['access_token']
        fehlerstandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text")
        JSONSamplePath = Path(cwd, "A2WorkingSkrips/DataFiles/JSONsample.txt")
        print("cpstate starting")
        fehlerstandorteStatus = cpstate(fehlerstandorte, atoken, s, JSONSamplePath)
        print("cpstate finished")
        f = open(fehlerstandorteTxtPath,'w')
        f.write(json.dumps(fehlerstandorteStatus))
window.close()