import glob, os
from PDFreader import readServiceProt

path_dir = "X:/Proj/V/V0019/E_Mobility_Charging_Solutions/06_IT Systeme/05 Non-Automotive Stammdatenbank/04_DC_Ladehardware/04_Serviceprotokolle"
for root, dirs, files in os.walk(path_dir):
    for dir in dirs:
        path_dir_dir = path_dir + "/" + dir
        #print(path_dir_dir)
        for root, dirs, files in os.walk(path_dir_dir):
            for file in files:
                #print(file)
                if file.endswith('.pdf'):
                    #print(file)
                    path_dir_dir_pdf = str(path_dir_dir) + "/" + str(file)
                    print(path_dir_dir_pdf)
                    readServiceProt(path_dir_dir_pdf)