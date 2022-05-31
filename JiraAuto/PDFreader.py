# importing required modules
import PyPDF4
import pprint
import os
from os.path import exists

def readServiceProt(Path, keyList):
    error = False
    fileName = Path.split("/")[-1]
    dirName = Path.split("/")[-2]
    feedBack = [dirName, fileName, "no entry", "empty", "empty", "empty", "empty", "empty", "empty"]
    # creating a pdf file object
    if exists(Path):
        pdfFileObj = open(Path, 'rb')

        # creating a pdf reader object
        try:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
        except:
            pdfReader = None

        if pdfReader != None:
            # printing number of pages in pdf file
            print(pdfReader.numPages)

            # creating a page object
            pageObj = pdfReader.getPage(0)

            # create a field object
            fieldObj = pdfReader.getFields()

            if fieldObj != None:
                if len(fieldObj) > 0:
                    i = 3
                    feedBack[2] = "found"
                    for key in keyList:
                        try:
                            vValue = fieldObj[key]["/V"]
                        except:
                            vValue = "Leer"
                        feedBack[i] = vValue
                        i = i + 1
                else:
                    print("fehlerhaft")
                    error = True
            else:
                print("fehlerhaft")
                error = True

        # closing the pdf file object
        pdfFileObj.close()
        if error:
            feedBack[2] = "unfindable"
        return feedBack
    else:
        print("Datei Existiert nicht")
        feedBack[2] = "unfindable"
        return feedBack

if __name__ == "__main__":
    UserName = os.getlogin()
    path = "X:/Proj/V/V0019/E_Mobility_Charging_Solutions/06_IT Systeme/05 Non-Automotive Stammdatenbank/04_DC_Ladehardware/04_Serviceprotokolle/132_Bergamo_20210928/07_04_Annex_I_Service_Report_KLL_Template_en 01-09-2021.pdf"
    #path = "C:\\Users\\" + str(UserName) + "\\Downloads\\TEST_PDF_Lesen.pdf"
    keyList = ["KLL_dealerID", "KLL_location","Ort Datum", "KLL_causeError", "KLL_customerComplaint", "KLL_detailedError"]
    failedReads = []
    successfulReads = []
    print(readServiceProt(path, keyList))