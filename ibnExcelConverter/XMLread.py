
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
def ridOf(sheet, relSheet, drawing):
    xmldoc = minidom.parse(sheet)
    stringlist = xmldoc.getElementsByTagName('control')
    print(len(stringlist))
    print(stringlist[0].attributes['name'].value)
    for x in stringlist:
        #print(x.attributes['r:id'].value,x.attributes['name'].value,x.attributes['shapeId'].value)
        relOf(x.attributes['r:id'].value, relSheet)
        nameOf(x.attributes['shapeId'].value, drawing)

def relOf(rid, relSheet ):
    xmldoc = minidom.parse(relSheet)
    stringlist = xmldoc.getElementsByTagName('Relationship')
    #print(len(stringlist))
    #print(stringlist[0].attributes['name'].value)
    for x in stringlist:
        if rid == x.attributes['Id'].value:
            print(x.attributes['Target'].value)
def nameOf(shapeId, drawing):
    xmldoc = minidom.parse(drawing)
    stringlist = xmldoc.getElementsByTagName('xdr:cNvPr')
    stringlist2 = xmldoc.getElementsByTagName('a:t')
    # print(len(stringlist))
    # print(stringlist[0].attributes['name'].value)
    for x in stringlist:
        if shapeId == x.attributes['id'].value:
            print(x.attributes['Target'].value)

if __name__ == "__main__":
    UserName = os.getlogin()

    drawing = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\drawings\\drawing1.xml"
    sheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\sheet1.xml"
    ctrPropsDir = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\ctrProps"
    relSheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\_rels\\sheet1.xml.rels"
    #xlsxPfad = "C:/Users/AJ2MSGR/OneDrivea - Dr.Ing.h.c.F.Porsche AG/IBN_Kastenfinden.xlsm"
    ridOf(sheet, relSheet, drawing)