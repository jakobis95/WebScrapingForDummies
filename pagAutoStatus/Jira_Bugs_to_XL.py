import json
import os
from openpyxl import load_workbook, styles
from openpyxl.styles import Font, Color
from openpyxl.styles import Alignment
from A3SupportingGeneralFunctions.NavigateInExcel import searchXL
from datetime import datetime
import pandas as pd
def create_active_issue_String(LastUpdate,IssueKey,Summary,IssueStatus):
    Stringg = "jello"
    print(Stringg)
def write_Bugs_to_XL(jira_xlsxPfad, xlsxPfad):
    wb = load_workbook(filename=xlsxPfad)
    Status = wb["StatusKurz"]
    wbMaster = load_workbook(filename=jira_xlsxPfad)
    JiraBugs = wbMaster["Sheet1"]
    activeTicketsCord = searchXL(Status, "active Tickets")
    activeTicketsColumn = activeTicketsCord[1]
    activeTicketsRow = activeTicketsCord[0]
    wbEpicNumber = searchXL(Status,"Epic Ticket Nummer", activeTicketsCord[0],"row")
    wbEpicNumberCol = wbEpicNumber[1]
    print("activeTicket Col", activeTicketsColumn)
    EpicLink = searchXL(JiraBugs, "Epic Link")
    EpicLinkColumn = EpicLink[1]
    columnDict ={}
    for x in range(3):
        i=1
        while JiraBugs.cell(row=EpicLink[0], column=i).value != None:
            print(JiraBugs.cell(row=1, column=i).value)
            columnDict[JiraBugs.cell(row=1, column=i).value] = i
            i = i + 1
        print(columnDict)
        i = 1
        while JiraBugs.cell(row=i, column= columnDict["Epic Link"]).value != None:
            searchResponse = searchXL(Status, JiraBugs.cell(row=i, column=columnDict["Epic Link"]).value, wbEpicNumberCol, "col")
            if searchResponse[0] != "notFound":
                print(JiraBugs.cell(row=i, column=columnDict["Epic Link"]).value, "found in Row:", searchResponse[0])
                if Status.cell(row=searchResponse[0] ,column=activeTicketsColumn ).value != None:
                    FirstValue = Status.cell(row=searchResponse[0] ,column=activeTicketsColumn ).value
                    print(FirstValue)
                    SummaryStr = str(FirstValue) + str(JiraBugs.cell(row=i, column=columnDict["Summary"]).value) + "\n"
                else:
                    SummaryStr = str(JiraBugs.cell(row=i, column=columnDict["Summary"]).value) + "\n"
                #SummaryStr = "\n" + str(JiraBugs.cell(row=i, column=columnDict["Summary"]).value)
                Status.cell(row=searchResponse[0] ,column=activeTicketsColumn ).value = SummaryStr
                Status.cell(row=searchResponse[0] ,column=activeTicketsColumn ).alignment = Alignment(wrapText=True)
            else:
                print(JiraBugs.cell(row=i, column=columnDict["Epic Link"]).value, " Not found")
            i = i + 1

    wb.save(xlsxPfad)
    wbMaster.save(jira_xlsxPfad)
if __name__ == "__main__":
    UserName = os.getlogin()
    jira_CSV_Path = "C:\\Users\\" + str(UserName) + "\\Downloads\\CurrentBugs18052022.xlsx"
    xlsxPfad = "C:\\Users\\" + str(UserName) + "\\Downloads\\IBN_SANDboxErweitert.xlsx"
    write_Bugs_to_XL(jira_CSV_Path, xlsxPfad)
