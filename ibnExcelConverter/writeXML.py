
from xml.dom import minidom
from XMLread import followXMLPath

xmlSheetPath =  "C:\\Users\\AJ2MSGR\\Documents\\ads-tec_ZSBPCB_20210923_TEMPLATE.xml"
xmldoc = minidom.parse(xmlSheetPath)
startNode = xmldoc.getElementsByTagName("ZSB_PCB")
path = ["ITEM","CHARGE_BOX","IDENT"]
parent = startNode[0]
result = followXMLPath(parent, path)
node = result[1].firstChild
node.data = "tschau"
xmldoc.writexml(open('data.xml', 'w'),indent="  ",addindent="  ",newl='\n')
print(result[1].firstChild)