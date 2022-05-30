# importing required modules
import PyPDF4
import pprint
import os
from os.path import exists

def readServiceProt(Path):

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

            # try:
            #     fieldObj
            # except NameError:
            #     fieldObj = {"error" : "error" }

            if fieldObj != None:
                if len(fieldObj) > 0:
                    print(fieldObj["KLL_dealerID"])
                    print(fieldObj["KLL_location"])
                    print(fieldObj["KLL_detailedError"])
                else:
                    print("fehlerhaft")
            else:
                print("fehlerhaft")
            #format dict nicely

            # Prints the nicely formatted dictionary
            #pprint.pprint(fieldObj)

            # Sets 'pretty_dict_str' to the formatted string value
            pretty_dict_str = pprint.pformat(fieldObj)

            #for field in fieldObj:
            #print(fieldObj["KLL_dealerID"])
            # closing the pdf file object
        pdfFileObj.close()
    else:
        print("Datei Existiert nicht")
        return "error"

if __name__ == "__main__":
    UserName = os.getlogin()
    path = "X:/Proj/V/V0019/E_Mobility_Charging_Solutions/06_IT Systeme/05 Non-Automotive Stammdatenbank/04_DC_Ladehardware/04_Serviceprotokolle/132_Bergamo_20210928/07_04_Annex_I_Service_Report_KLL_Template_en 01-09-2021.pdf"
    #path = "C:\\Users\\" + str(UserName) + "\\Downloads\\FehlerhaftePDF.pdf"
    readServiceProt(path)