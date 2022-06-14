
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def findChild(parent, childLocalName):
    for child in parent._get_childNodes():
        if child._get_localName() == childLocalName:
            return True, child
    return False, child

def followXMLPath(parent, path):
    for localName in path:
        print(localName)
        result = findChild(parent, localName)
        if result[0] == True:
            parent = result[1]
        else:
            return result
    return result

def relOf(rid, relSheet ):
    xmldoc = minidom.parse(relSheet)
    stringlist = xmldoc.getElementsByTagName('Relationship')
    #print(len(stringlist))
    #print(stringlist[0].attributes['name'].value)
    for x in stringlist:
        if rid == x.attributes['Id'].value:
            print(x.attributes['Target'].value)
    return x.attributes['Target'].value

def nameOf(shapeId, drawing):
    xmldoc = minidom.parse(drawing)
    finds = xmldoc.getElementsByTagName('xdr:cNvPr')

    i = 0
    for element in finds:
        if element.attributes['id'].value == shapeId and element.attributes['name'].value[0:5] == "Check":
            print(element.attributes['name'].value)
            while element._get_localName() != "sp":
                i = i + 1
                element = element.parentNode
            print(element._get_localName())
            pathToCheckBoxText = ["txBody", "p", "r", "t"]
            result = followXMLPath(element, pathToCheckBoxText)
            if result[0]:
                print(result[1].firstChild.nodeValue)

            #print(shapeId, "=", element.firstChild.nodeValue)

def ridOf(sheet, relSheet, drawing):
    xmldoc = minidom.parse(sheet)
    stringlist = xmldoc.getElementsByTagName('control')
    print(len(stringlist))
    print(stringlist[0].attributes['name'].value)
    checkBoxList = []
    for x in stringlist:
        checkBox = [x.attributes['r:id'].value, x.attributes['shapeId'].value, "", "", ""]
        checkBox[2] = relOf(x.attributes['r:id'].value, relSheet)
        result = nameOf(x.attributes['shapeId'].value, drawing)
        print(result[1])

if __name__ == "__main__":
    UserName = os.getlogin()

    drawing = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\drawings\\drawing1.xml"
    sheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\sheet1.xml"
    ctrPropsDir = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\ctrProps"
    relSheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\_rels\\sheet1.xml.rels"
    #xlsxPfad = "C:/Users/AJ2MSGR/OneDrivea - Dr.Ing.h.c.F.Porsche AG/IBN_Kastenfinden.xlsm"
    ridOf(sheet, relSheet, drawing)