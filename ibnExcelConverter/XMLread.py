
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
def isChecked(ctrPropsDir, ctrPropXML):
    print()
    if ctrPropXML.split("/")[1] != "ctrlProps":
        print("nicht in Folder controlProps")
        return False
    else:
        path = ctrPropsDir + "\\" + ctrPropXML.split("/")[2]
        xmldoc = minidom.parse(path)
        stringlist = xmldoc.getElementsByTagName('formControlPr')
        stringlist = stringlist[0]
        print(stringlist.attributes.values)
        keys = stringlist.attributes.keys()
        for key in keys:
            if key == "checked":
                print(stringlist.attributes["checked"].value)
                return True
        else:
            return False

def relOf(rid, relSheet ):
    xmldoc = minidom.parse(relSheet)
    stringlist = xmldoc.getElementsByTagName('Relationship')
    #print(len(stringlist))
    #print(stringlist[0].attributes['name'].value)
    for x in stringlist:
        if rid == x.attributes['Id'].value:
            print(x.attributes['Target'].value)
            return x.attributes['Target'].value
    return "not found"

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
                return result[1].firstChild.nodeValue
    return "has no name"
            #print(shapeId, "=", element.firstChild.nodeValue)

def ridOf(sheet, relSheet, drawing, ctrPropsDir):
    xmldoc = minidom.parse(sheet)
    stringlist = xmldoc.getElementsByTagName('control')
    print(len(stringlist))
    print(stringlist[0].attributes['name'].value)
    checkBoxList = []
    for x in stringlist:
        checkBox = [x.attributes['r:id'].value, x.attributes['shapeId'].value, "", "", ""]
        checkBox[2] = relOf(x.attributes['r:id'].value, relSheet)
        checkBox[3] = nameOf(x.attributes['shapeId'].value, drawing)
        checkBox[4] = isChecked(ctrPropsDir, checkBox[2])
        print(checkBox)
        checkBoxList.append(checkBox)
    for checkBox in checkBoxList:
        if checkBox[3] != "has no name":
            print(checkBox)

if __name__ == "__main__":
    UserName = os.getlogin()

    drawing = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\drawings\\drawing1.xml"
    sheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\sheet1.xml"
    ctrPropsDir = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\ctrlProps"
    relSheet = "C:\\Users\\AJ2MSGR\\Documents\\swindon cbx commissioning\\xl\\worksheets\\_rels\\sheet1.xml.rels"
    #xlsxPfad = "C:/Users/AJ2MSGR/OneDrivea - Dr.Ing.h.c.F.Porsche AG/IBN_Kastenfinden.xlsm"
    ridOf(sheet, relSheet, drawing, ctrPropsDir)