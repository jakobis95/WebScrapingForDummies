from openpyxl import load_workbook, styles
import os

def main(xlsxPfad):

    wb = load_workbook(filename=xlsxPfad, keep_vba=True)
    IBN_S = wb["IBN-Stammdaten"]
    for i in range(1,20,1):
        print(i)
        #IBN_S.cell(row=46, column=i).value = "Hello"
        print(IBN_S.cell(row=46, column=i).value)

    #wb.save(xlsxPfad)
if __name__ == "__main__":
    UserName = os.getlogin()
    xlsxPfad = "C:\\Users\\AJ2MSGR\\Documents\\IBMtoXMLProjectData\\swindon cbx commissioning.xlsm"
    main(xlsxPfad)