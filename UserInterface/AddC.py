import os
from openpyxl import load_workbook, styles
from openpyxl.styles import Font, Color
from A3SupportingGeneralFunctions.NavigateInExcel import searchXL
from datetime import datetime
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo


def addShit(ws):
    ws.append(["Fruit", "2011", "2012", "2013", "2014"])

    data = [
        ['Apples', 10000, 5000, 8000, 6000],
        ['Pears', 2000, 3000, 4000, 5000],
        ['Bananas', 6000, 6000, 6500, 6000],
        ['Oranges', 500, 300, 200, 700],
    ]
    for row in data:
        ws.append(row)
    tab = Table(displayName="Table1", ref="A1:E5")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    tab.tableStyleInfo = style
    ws.add_table(tab)

def addCol(ws):
    ws.insert_cols(2)
    ws.cell(row=1,column=2).value = "Hello"
def update(xlsxPfad, sheet):
    wb = load_workbook(filename=xlsxPfad)
    ws = wb[sheet]
    wb.save(xlsxPfad)
    return wb,ws

def replaceTab(ws, wb, xlsxPfad, ref, displayName):
    autofilter = ws.tables[displayName].autoFilter
    style = ws.tables[displayName].tableStyleInfo

    tab = Table(displayName=displayName, ref=ref)
    #style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    tab.tableStyleInfo = style
    ws.tables[displayName] = tab
    #ws.cell(row=13, column=59).value = "Changed"
    wb.save(xlsxPfad)

if __name__ == "__main__":
    UserName = os.getlogin()
    xlsxPfad = "C:\\Users\\" + str(UserName) + "\\Downloads\\book12.xlsx"
    wb = load_workbook(filename=xlsxPfad)

    ws = wb["Sheet1"]
    #addShit(ws)
    #table._initialise_columns()
    wb.save(xlsxPfad)
    os.startfile(xlsxPfad)
