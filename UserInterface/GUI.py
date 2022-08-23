import PySimpleGUI as sg
from pathlib import Path
import os
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
downloads = Path(Path.home(), "Downloads")
jira_xlsx_path_HVAC = Path(downloads, "HVACOverview.xlsx")
jira_xlsx_path_VR16 = jira_xlsx_path_HVAC.with_name("VR16UpdatedStations.xlsx")
master_xlsx_path = jira_xlsx_path_HVAC.with_name("IBN_Tracking.xlsx")
jira_CSV_Path = jira_xlsx_path_HVAC.with_name("current_bugs.xlsx")

layout = [
    [sg.Button("Start", font=["Helvetica", 15], button_color='green', size=(20,1))],
    [sg.Text("Wochenübersichtstabelle", size=(15,1)),sg.Input(default_text=master_xlsx_path, key="-XL-"),sg.FileBrowse()],
    [sg.Text("HVAC xlsx Datei", size=(15,1)),sg.Input(default_text=jira_xlsx_path_HVAC, key="-XL-"),sg.FileBrowse()],
    [sg.Text("VR16 xlsx Datei", size=(15,1)),sg.Input(default_text=jira_xlsx_path_VR16, key="-XL-"),sg.FileBrowse()],
    [sg.Text("Current Bugs Datei", size=(15,1)),sg.Input(default_text=jira_CSV_Path, key="-XL-"),sg.FileBrowse()],
    [sg.Text("Teilfunktionen:",font=("Helvetica",15))],
    [sg.Button("Update Locations",size=(30,1))],
    #[sg.Button("get Path")],
    [sg.Button("Excel mit CBX Status befüllen",size=(30,1))],
    [sg.Button("HVAC und VR16 von Jira eintragen",size=(30,1))],
    [sg.Button("Current Bugs von Jira eintragen",size=(30,1))],
    [sg.Button("Exit", button_color="red", size=(30,1))]
]

# create the window
window = sg.Window("CDUT", layout)

# pre fill Input field

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