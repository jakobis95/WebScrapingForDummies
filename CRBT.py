## Python Packages: hier sollte nicht rot unterstrichen sein auch nicht wenn der text ausgegraut sein sollte.
import PySimpleGUI as sg                                # PySimpleGUI Package
from urllib3.exceptions import InsecureRequestWarning   # urllib3 Package
from urllib3 import disable_warnings                    # urllib3 Package
from openpyxl import styles                             # openpyxlPackage
import openpyxl_utilities                               # openpyxl_utilities Package
import requests                                         # requests Package
## ende Python Packages

#Standard
from pathlib import Path                                # in standardmaeßig enthalten
import os                                               # in standardmaeßig enthalten
import webbrowser                                       # in standardmaeßig enthalten
# ende Standard

from A1_Working_Skripts.main import updateLocations, fillCBXStatusCtrl, updateVR16_HVAC, updateCurrentBugs, jiraEpicAbgleich
from A2_Working_Support_Functions.FileManagementTools import check_files_timeliness
# Path needed
disable_warnings(InsecureRequestWarning)
cwd = Path().cwd()
fehlerstandorteTxtPath = Path(cwd, "A1_Working_Skripts/DataFiles/fehlerstandorteStatus.text")
offlinestandorteTxtPath = Path(cwd, "A1_Working_Skripts/DataFiles/offlinestandorte.text")
tokenPath = Path(cwd, "A1_Working_Skripts/DataFiles/refreshtoken.txt")
JSONSamplePath = Path(cwd, "A1_Working_Skripts/DataFiles/JSONsample.txt")
#Temp Programm parts
UserName = os.getlogin()
downloads = Path(Path.home(), "Downloads")
jira_xlsx_path_HVAC = Path(downloads, "HVAC_OK.xlsx")
jira_xlsx_path_VR16 = jira_xlsx_path_HVAC.with_name("VR16_OK.xlsx")
master_xlsx_path = jira_xlsx_path_HVAC.with_name("IBN_Tracking.xlsx")
jira_CSV_Path = jira_xlsx_path_HVAC.with_name("Offene_Tickets.xlsx")
jira_Master_XLSX = jira_xlsx_path_HVAC.with_name("DO_NOT_TOUCHE_JIRA_MASTERLISTE.xlsx")

w = 80
h = 1
layout = [
    [sg.Button("Start", font=["Helvetica", 15], button_color='green', size=(20,1))],
    [sg.Text("Wochenübersicht:", size=(15,1)),sg.Input(default_text=master_xlsx_path, key="-XL-", size=(w,h)),sg.FileBrowse()],
    [sg.Text("HVAC xlsx Datei:", size=(15,1)),sg.Input(default_text=jira_xlsx_path_HVAC, key="-HVAC-", size=(w,h)),sg.FileBrowse()],
    [sg.Text("VR16 xlsx Datei:", size=(15,1)),sg.Input(default_text=jira_xlsx_path_VR16, key="-VR16-", size=(w,h)),sg.FileBrowse()],
    [sg.Text("Current Bugs Datei:", size=(15,1)),sg.Input(default_text=jira_CSV_Path, key="-Current-", size=(w,h)),sg.FileBrowse()],
    [sg.Text("Jira Master Datei:", size=(15,1)),sg.Input(default_text=jira_Master_XLSX, key="-Master-", size=(w,h)),sg.FileBrowse()],
    [sg.Text("Teilfunktionen:",font=("Helvetica",15))],
    [sg.Button("Start ohne CPM Status updaten", button_color='lightgreen', size=(30,1))],
    [sg.Button("CPM Status updaten",size=(30,1))],
    [sg.Button("CBX Zustand in Excel aktualisieren",size=(30,1))],
    [sg.Button("HVAC und VR16 von Jira eintragen",size=(30,1))],
    [sg.Button("Offene Tickets von Jira eintragen",size=(30,1))],
    [sg.Button("Jira Epic Abgleich",size=(30,1))],
    [sg.Text('_'*120)],
    [sg.Button("Exit", button_color="red", size=(30,1)), sg.Button("Anleitung", size=(30,1))]
]

# create the window
window = sg.Window("CBRT", layout)

# pre fill Input field

# create an event loop
while True:
    event, values = window.read()
    # End prozess if user closes Window
    # presses the OK button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "VR16":
        webbrowser.open('https://skyway.porsche.com/jira/issues/?filter=62078')
    if event == "HVAC":
        webbrowser.open("https://skyway.porsche.com/jira/issues/?filter=60839")
    if event == "Bugs":
        webbrowser.open("https://skyway.porsche.com/jira/issues/?filter=60218")
    if event == "Start":
        input("Wurde eine Spalte für den heutigen Tag angelegt? Bitte mit Enter bestätigen.")
        input("Stellen Sie sicher dass Sie nicht im Porsche Wlan/Netzwerk sind? Bitte mit Enter bestätigen.")
        files = [values["-HVAC-"], values["-VR16-"], values["-XL-"]]
        if check_files_timeliness(files) != True:
            print("Ihre Jira Dateien sind nicht aktuell und ihr skript wurde beendet")
            exit()
        updateLocations(tokenPath, offlinestandorteTxtPath, fehlerstandorteTxtPath, JSONSamplePath)
        fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, values["-XL-"])
        updateVR16_HVAC(values["-HVAC-"], values["-VR16-"], values["-XL-"])
        updateCurrentBugs(values["-Current-"], values["-XL-"])
        # Finished Prozess open complete file
        os.startfile(values["-XL-"])
        sg.popup("Prozess Fertig")
    if event == "get Path":
        fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, values["-XL-"])
        updateVR16_HVAC(values["-HVAC-"], values["-VR16-"], values["-XL-"])
        updateCurrentBugs(values["-Current-"], values["-XL-"])
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "CPM Status updaten":
        updateLocations(tokenPath, offlinestandorteTxtPath, fehlerstandorteTxtPath, JSONSamplePath)
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "CBX Zustand in Excel aktualisieren":
        fillCBXStatusCtrl(fehlerstandorteTxtPath, offlinestandorteTxtPath, values["-XL-"])
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "HVAC und VR16 von Jira eintragen":
        updateVR16_HVAC(values["-HVAC-"], values["-VR16-"], values["-XL-"])
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "Offene Tickets von Jira eintragen":
        updateCurrentBugs(values["-Current-"], values["-XL-"])
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "Jira Epic Abgleich":
        jiraEpicAbgleich(values["-Master-"], values["-XL-"])
        sg.popup("Prozess Fertig")
        os.open(master_xlsx_path)
    if event == "Anleitung":
        os.system("ChargeBoxReportingTool_Anleitung.pdf")


window.close()