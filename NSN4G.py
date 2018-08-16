import xml.etree.ElementTree as ET
import os

xmlfile='D:/sdataprj/Full/Full/4G/NSN/4G NSN.xml'
ns = {'ns0': 'raml20.xsd'}

element_tree = ET.iterparse(xmlfile, events=('start', ))
#test = ET.parse("1.xml")
#root = test.getroot()
#print(root.find('.//ns0:managedObject', ns).tag)
header = ""

for event, elem in element_tree:
    if elem.tag.split("}")[-1] == "header":
        header = ET.tostring(elem)
        break
#root = element_tree.getroot()

def splitFunction():

    MOCount = 0
    contentPerFile = ""
    i = 0
    fileIndex = 0
    for event, elem in element_tree:
        
        if elem.tag.split("}")[-1] == 'managedObject':
            MOCount += 1
            contentPerFile += str(ET.tostring(elem), 'utf-8')
            
            #print("loading")
            if MOCount == 20000:
                writeXML(fileIndex, contentPerFile, header)
            
                MOCount = 0
                contentPerFile = ""
                fileIndex += 1

        elem.clear()   
        i += 1     

    writeXML(fileIndex, contentPerFile, header)        


def writeXML(fileIndex, contenPerFile, header):
    XMLFileName = format(str(fileIndex) + ".xml")
    with open(XMLFileName, 'w', encoding='utf-8') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE raml SYSTEM \'raml20.dtd\'>\n<raml version=\"2.0\" xmlns=\"raml20.xsd\">\n<cmData type=\"actual\">\n")
        f.write(str(header,'utf-8'))
        f.write(contenPerFile)
        f.write("</cmData>\n</raml>")

splitFunction()
#print(root.tag)
#fileName = xmlfile.split('/')[-1]
#get data time
#dateTimeTag = root.find("")
#with open("num.xml", 'w') as f:
#    f.write(header)