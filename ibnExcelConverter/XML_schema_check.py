from xml.dom import minidom
import os
import xmlschema

def is_XML_correct(xml_schema, xml):
    my_schema = xmlschema.XMLSchema('C:\\Users\\AJ2MSGR\\Documents\\ZSB_PCB - Kopie.xsd')
    print(my_schema.is_valid(xml))
    my_schema.validate(xml)

if __name__ == "__main__":
    my_schema = "C:\\Users\\AJ2MSGR\\Documents\\ZSB_PCB - Kopie.xsd"
    my_xml = "data.xml"
    is_XML_correct(my_schema, my_xml)