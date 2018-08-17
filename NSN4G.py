import xml.etree.ElementTree as ET
import os
import time


xmlfile='D:/sdataprj/Full/Full/4G/NSN/4G NSN.xml'
ns = {'ns0': 'raml20.xsd'}

element_tree = ET.iterparse(xmlfile, events=('start', ))
#test = ET.parse("1.xml")
#root = test.getroot()
#print(root.find('.//ns0:managedObject', ns).get('class'))

header = ""


for event, elem in element_tree:
    if elem.tag.split("}")[-1] == "header":
        header = ET.tostring(elem)
        break

def splitFunction2():
    start_time = time.time()
    MOCount = 0
    contentPerFile = []
    
    fileIndex = 0
    for _, elem in element_tree:
        if elem.tag == '{raml20.xsd}managedObject':
            MOCount += 1
            #print(MOCount)
            contentPerFile.append(ET.tostring(elem))
            
            if MOCount == 120000:
                stri = makeString(contentPerFile)

                writeSplitedXML(fileIndex, stri, header)
            
                MOCount = 0
                contentPerFile = []
                fileIndex += 1

        elem.clear()   
            
    stri = makeString(contentPerFile)
    writeSplitedXML(fileIndex, stri, header)
    print("--- %s seconds ---" % (time.time() - start_time))

def makeString(contentPerFile):
    arrayToWrite = []
    for content in contentPerFile:
        arrayToWrite.append(str(content, 'utf-8'))
    
    stri = "".join(arrayToWrite)
    return stri


def writeSplitedXML(fileIndex, contenPerFile, header):
    XMLFileName = format(str(fileIndex) + ".xml")
    with open(XMLFileName, 'w', encoding='utf-8') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE raml SYSTEM \'raml20.dtd\'>\n<raml version=\"2.0\" xmlns=\"raml20.xsd\">\n<cmData type=\"actual\">\n")
        f.write(str(header,'utf-8'))
        f.write(contenPerFile)
        f.write("</cmData>\n</raml>")
def ParseFuction(xmlURL):
    root = ET.parse(xmlURL).getroot()
    
splitFunction2()
#print(root.tag)
#fileName = xmlfile.split('/')[-1]
#get data time
#dateTimeTag = root.find("")
#with open("num.xml", 'w') as f:
#    f.write(header)