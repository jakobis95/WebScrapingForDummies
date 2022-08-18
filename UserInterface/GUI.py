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
from Main import updateLocations, fillCBXStatusCtrl, updateVR16_HVAC, updateCurrentBugs
from A3SupportingGeneralFunctions.FileManagementTools import askForToken, check_files_timeliness
# Path needed
disable_warnings(InsecureRequestWarning)
cwd = Path().cwd().parent
fehlerstandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/fehlerstandorteStatus.text")
offlinestandorteTxtPath = Path(cwd, "A2WorkingSkrips/DataFiles/offlinestandorte.text")
tokenPath = Path(cwd, "A2WorkingSkrips/DataFiles/refreshtoken.txt")
JSONSamplePath = Path(cwd, "A2WorkingSkrips/DataFiles/JSONsample.txt")
#Temp Programm parts
UserName = os.getlogin()
jira_xlsx_path_HVAC = "C:\\Users\\" + str(UserName) + "\\Downloads\\HVACOverview.xlsx"
jira_xlsx_path_VR16 = "C:\\Users\\" + str(UserName) + "\\Downloads\\VR16UpdatedStations.xlsx"
master_xlsx_path = "C:\\Users\\" + str(UserName) + "\\Downloads\\IBN_Tracking.xlsx"
jira_CSV_Path = "C:\\Users\\" + str(UserName) + "\\Downloads\\current_bugs.xlsx"

layout = [
    [sg.Text("CBX Doc Update Tool")],
    [sg.Button("Run All")],
    [sg.Button("Update Locations")],
    [sg.Button("get Path")],
    [sg.Button("Excel mit CBX Status befüllen")],
    [sg.Button("HVAC und VR16 von Jira eintragen")],
    [sg.Button("Current Bugs von Jira eintragen")],
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
        files = [jira_xlsx_path_VR16, jira_xlsx_path_HVAC, jira_CSV_Path]
        if check_files_timeliness(files) != True:
            print("Ihre Jira Dateien sind nicht aktuell und ihr skript wurde beendet")
            exit()
        updateLocations(tokenPath, offlinestandorteTxtPath, fehlerstandorteTxtPath, JSONSamplePath)
        fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, master_xlsx_path)
        updateVR16_HVAC(jira_xlsx_path_HVAC, jira_xlsx_path_VR16, master_xlsx_path)
        updateCurrentBugs(jira_CSV_Path, master_xlsx_path)
        # Finished Prozess open complete file
        os.startfile(master_xlsx_path)
        sg.popup("Prozess Fertig")
    if event == "get Path":
        cwd = Path().cwd().parent
        print(Path(cwd, "A2WorkingSkrips/DataFiles/refreshtoken.txt"))

    if event == "Update Locations":
        updateLocations(tokenPath, offlinestandorteTxtPath, fehlerstandorteTxtPath, JSONSamplePath)
    if event == "Excel mit CBX Status befüllen":
        fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, master_xlsx_path)
    if event == "HVAC und VR16 von Jira eintragen":
        updateVR16_HVAC(jira_xlsx_path_HVAC, jira_xlsx_path_VR16, master_xlsx_path)

    if event == "Current Bugs von Jira eintragen":
        updateCurrentBugs(jira_CSV_Path, master_xlsx_path)


window.close()