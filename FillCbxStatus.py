import json
from Runner import refreshT
from openpyxl import Workbook,load_workbook
import requests
from NavigateInExcel import searchXL, conditional_formatting_with_rules
from datetime import datetime

def WriteStatusToXL(xlsxPfad, offlineCBX, fehlerCBX):
    cp = 0
    wb = load_workbook(filename=xlsxPfad)
    todayCbxCounter = 1
    StatusWB = wb["cbxStatusListe"]
    TodayFehlerWB = wb["overviewToday"]
    LastRow = StatusWB.max_row
    #TodayColumnString = "Fehlerhaft am " + datetime.today().strftime('%d.%m.%Y')
    TodayColumnString = "Fehlerhaft am 25.01.2022"
    #finds Column with the date of today
    TodayColumn = searchXL(StatusWB, TodayColumnString)[1]
    #finds Column to display if cp1 and/or cp2 has a problem
    cp1Column = searchXL(StatusWB, "1")[1]
    cp2Column = searchXL(StatusWB, "2")[1]
    cpColumn = [cp1Column,cp2Column]

    if TodayColumn != "notFound":
        print("XX today Column is:", TodayColumn)
        #Fill in all destinations that are currently offline
        for item in offlineCBX['content']:
            if item['uniqueId'][17] == "1":
                cp = 0
                searchTerm = item['uniqueId']
            else:
                cp = 1
                searchTerm = item['uniqueId']
                searchTerm = searchTerm[:17] + "1"

            foundRow = searchXL(StatusWB, searchTerm, 1, "col")[0]
            print("XX ", foundRow)
            if foundRow != "notFound":
                StatusWB.cell(row=foundRow, column=TodayColumn).value = "offline"
                StatusWB.cell(row=foundRow, column=cpColumn[cp]).value = "x"
                TodayFehlerWB.cell(row=todayCbxCounter, column=1).value = item['uniqueId']
                TodayFehlerWB.cell(row=todayCbxCounter, column=2).value = 'Gefunden'
            else:
                TodayFehlerWB.cell(row=todayCbxCounter, column=1).value = item['uniqueId']
                TodayFehlerWB.cell(row=todayCbxCounter, column=2).value = 'nicht Gefunden'
            TodayFehlerWB.cell(row=todayCbxCounter, column=3).value = 'Offline'
            todayCbxCounter = todayCbxCounter + 1

        # Fill in all destinations that currently have a failure
        for item in fehlerCBX['content']:
            if item['uniqueId'][17] == "1":
                cp = 0
                searchTerm = item['uniqueId']
            else:
                cp = 1
                searchTerm = item['uniqueId']
                searchTerm = searchTerm[:17] + "1"

            foundRow = searchXL(StatusWB, searchTerm, 1, "col")[0]
            print("XX ", foundRow)
            if foundRow != "notFound":
                StatusWB.cell(row=foundRow, column=TodayColumn).value = "j"
                StatusWB.cell(row=foundRow, column=cpColumn[cp]).value = "x"
                TodayFehlerWB.cell(row=todayCbxCounter, column=1).value = item['uniqueId']
                TodayFehlerWB.cell(row=todayCbxCounter, column=2).value = 'Gefunden'
            else:
                TodayFehlerWB.cell(row=todayCbxCounter, column=1).value = item['uniqueId']
                TodayFehlerWB.cell(row=todayCbxCounter, column=2).value = 'nicht Gefunden'
            TodayFehlerWB.cell(row=todayCbxCounter, column=3).value = 'Fehler'
            todayCbxCounter = todayCbxCounter + 1

    else:
        print("Es konnte kein Spalte mit dem heutigen Datum gefunden werden. Prüfen Sie die Excel-datei.")
    # print(searchXL(StatusWB, "Hello was geht"))
    wb.save(xlsxPfad)

#def WriteStatusToXL(offlineCBX, fehlerCBX, xlsxPfad):

if __name__ == "__main__":
    xlsxPfad = r"C:\Users\FO4A5OY\OneDrive - Dr. Ing. h.c. F. Porsche AG\LE_Failure_Analysis\CBX_Fehlerliste_AutoPyTesting.xlsx"
    f = open("fehler.json")
    fehlerCBX = json.load(f)

    f = open("offline.json")
    offlineCBX = json.load(f)

    #WriteStatusToXL(offlineCBX, fehlerCBX, xlsxPfad)
    #WriteStatusToXL( xlsxPfad, offlineCBX, offlineCBX)

    f = open("fehlerstandorteStatus.text", 'r')
    fehlerCBX = json.load(f)
    for element in fehlerCBX:
        print(element)

    f = open("offlinestandorte.text", 'r')
    offlineCBX = json.load(f)
    for element in offlineCBX:
        print(element)

    WriteStatusToXL(xlsxPfad, offlineCBX, offlineCBX)