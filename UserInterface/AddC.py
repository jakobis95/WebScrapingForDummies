import os
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


def addShit(ws):
    ws.append(["Fruit", "2011", "2012", "2013", "2014","2011", "2012", "2013", "2014"])

    data = [
        ['Apples', 10000, 5000, 8000, 6000],
        ['Pears', 2000, 3000, 4000, 5000],
        ['Bananas', 6000, 6000, 6500, 6000],
        ['Oranges', 500, 300, 200, 700],
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


def addCol(ws, colNr ,headerRow , headerVal):
    ws.insert_cols(colNr)
    ws.cell(row=headerRow, column=colNr).value = headerVal

def update(xlsxPfad, sheetName):
    wb = load_workbook(filename=xlsxPfad)
    ws = wb[sheetName]
    wb.save(xlsxPfad)
    return wb,ws

def replaceTab(ws, ref, displayName):
    #copys autofilter
    autofilter = ws.tables[displayName].autoFilter
    #copy current style
    style = ws.tables[displayName].tableStyleInfo
    #create new enlarged table
    entab = Table(displayName=displayName, ref=ref)
    entab.tableStyleInfo = style
    #change current table to new enlarged table
    ws.tables[displayName] = entab

if __name__ == "__main__":
    UserName = os.getlogin()
    xlsxPfad = "C:\\Users\\" + str(UserName) + "\\Downloads\\book1.xlsx"
    wb = load_workbook(filename=xlsxPfad)
    ws = wb["Sheet1"]

    addShit(ws)
    wb.save(xlsxPfad)
    wb, ws = update(xlsxPfad, "Sheet1")
    #add column in column 2
    addCol(ws, 2, 1, "NewCol1")
    # update table size
    replaceTab(ws, "A1:F5", "Table1")
    wb.save(xlsxPfad)
    #update workbook and worksheet
    wb, ws = update(xlsxPfad, "Sheet1")
    # add column in column 2
    addCol(ws, 2, 1, "NewCol2")
    #update table size
    replaceTab(ws, "A1:G5", "Table1")
    wb.save(xlsxPfad)
    os.startfile(xlsxPfad)
