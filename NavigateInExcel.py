from openpyxl import Workbook
import openpyxl
from datetime import datetime

def searchXL(ws, searchTerm, searchArea = 0, rowcol = "all"):
    Ycor = "notFound"
    Xcor = "notFound"

    if searchArea != 0 or rowcol != "all":
        if rowcol == "row":
            minRow = searchArea
            maxRow = minRow
            minCol = 0
            maxCol = ws.max_column
        elif rowcol =="col":
            minCol = searchArea
            maxCol = minCol
            minRow = 0
            maxRow = ws.max_row
    else:
        minCol = 0
        minRow = 0
        maxCol = ws.max_column
        maxRow = ws.max_row


    print("Fehlerhaft am " + datetime.today().strftime('%d.%m.'))
    # for row in ws.iter_rows(max_col=1, max_row=10):
    #     for cell in row:
    #         print(cell.value)
    #         if cell.value == "ID":
    #             print(cell.column)  # change column number for any cell value you want
    #             print("break")
    #             break

    for col in ws.iter_cols(min_row=minRow, max_row=maxRow, min_col=minCol, max_col= maxCol):
        for cell in col:
            if cell.value == searchTerm:
                Ycor = cell.row
                Xcor = cell.column
                print("Suchbegriff an Coordinate[" + str(cell.row) + "," + str(cell.column) + "] gefunden" )  # change column number for any cell value you want
                break

    if Xcor == "notFound":
        print("nichts gefunden")

    return Ycor, Xcor



if __name__ == "__main__":
    file = "NavigationSheet.xlsx"
    # wb = openpyxl.Workbook(file)
    wb = openpyxl.load_workbook(filename=file)
    ws = wb.worksheets[0]
    #searchTerm = "Fehlerhaft am " + datetime.today().strftime('%d.%m.%Y')
    searchTerm = "ID"
    Coordinates = searchXL(ws,searchTerm)
    wb.save('NavigationSheet.xlsx')