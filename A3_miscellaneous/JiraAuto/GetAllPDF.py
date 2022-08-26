import glob, os
from PDFreader import readServiceProt
import openpyxl
#Bevor dieses Skript gestartet werden kann, muss das in path_dir angezeigte Verzeichnis einmal aufgerufen worden sein
i = 1
UserName = os.getlogin()
keyList = ["KLL_dealerID", "KLL_location","KLL_date", "KLL_causeError", "KLL_customerComplaint", "KLL_detailedError"]
path_dir = "X:/Proj/V/V0019/E_Mobility_Charging_Solutions/06_IT Systeme/05 Non-Automotive Stammdatenbank/04_DC_Ladehardware/04_Serviceprotokolle"
path_xlsx = "C:\\Users\\" + str(UserName) + "\\Downloads\\1overviewServiveProtocol.xlsx"
path_xlsx_save = "C:\\Users\\" + str(UserName) + "\\Downloads\\XXoverviewServiveProtocol.xlsx"
wb = openpyxl.load_workbook(filename=path_xlsx)
ws = wb['Tabelle1']
for root, dirs, files in os.walk(path_dir):
    #Todo dirs ohne PDF ebenfalls erfassen als fehlerhaft
    for dir in dirs:
        path_dir_dir = path_dir + "/" + dir
        #print(path_dir_dir)
        for root, dirs, files in os.walk(path_dir_dir):
            for file in files:
                #print(file)
                if file.endswith('.pdf'):
                    #print(file)
                    k = 1
                    path_dir_dir_pdf = str(path_dir_dir) + "/" + str(file)
                    #print(path_dir_dir_pdf)
                    data = readServiceProt(path_dir_dir_pdf, keyList)
                    print(data)
                    for item in data:
                        ws.cell(row=i+1, column=k).value = str(item)
                        k = k + 1
                    i = i + 1
wb.save(path_xlsx_save)
