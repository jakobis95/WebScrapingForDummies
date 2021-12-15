from openpyxl import Workbook
import openpyxl

file = "NavigationSheet.xlsx"
#wb = openpyxl.Workbook(file)
wb = openpyxl.load_workbook(filename='NavigationSheet.xlsx')
ws = wb.active
i=0
for row in ws.iter_rows(min_row=1, max_col=3, max_row=2):
    for cell in row:
        print(cell)

wb.save('NavigationSheet.xlsx')