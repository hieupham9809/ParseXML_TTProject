import xml.etree.ElementTree as ET
import os
import time


xmlfile='D:/sdataprj/Full/Full/4G/NSN/4G NSN.xml'
ns = {'ns0': 'raml20.xsd'}
fileIndex = 0
network = '4G'
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
    #find all MO
    Type = root.findall(".//ns0:managedObject", ns)
    typeArray = []     #List of all MO Name
    for name in Type:
        typeArray.append(name.get('class'))
    nameOfObject = list(set(typeArray))
    #now we have a list name of MO

    #for each name of MO, take all MO which has this name:
    
    for dataTypeName in nameOfObject:
        print(dataTypeName)
        arrayOfContent = []
        for typeName in Type:
            if typeName.get('class') == dataTypeName:
                arrayOfContent.append(typeName)
        headerArray = createHeader()

        dataArray = []
        for content in arrayOfContent:
            dataArray.append(getContentOfObj(content))

        nameOfOutputFile = "export_" + dataTypeName + "__" + dateTime + ".txt"
        locationOfOutputFile ="NSN/" + network + "/" + dateTime + "/" + nameOfOutputFile
        if not os.path.exists(os.path.dirname(locationOfOutputFile)):
            try:
                os.makedirs(os.path.dirname(locationOfOutputFile))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
            
        exportFile = open(os.path.abspath(locationOfOutputFile), 'a', encoding='utf-8')
        headerToWrite = "".join(headerArray)
        exportFile.write(headerToWrite)

        contentToWrite = "".join(dataArray)
        #for data in dataArray:
        #    contentToWrite.append(data + "\n")
            #print(data)
        exportFile.write(contentToWrite)
        exportFile.close()    



def createHeader(content): #return array of header
    headerArray = []
    headerArray.append("FileName\t")
    headerArray.append("MO\t")
    if not content:
        return "".join(headerArray) + "\n"
    headerNames = content.findall("./*")

    
    if not headerNames:
        pass
    else:
        for headerName in headerNames:    
            elements = headerName.findall("./*")
            if not elements:
                headerArray.append(headerName.tag.split('}')[-1].rstrip() + "\t")
            else:
                currentTagName = headerName.tag.split('}')[-1].rstrip()
                for element in elements:
                    columnHeader = currentTagName + "_" + element.tag.split('}')[-1].rstrip()
                    headerArray.append(columnHeader + "\t")
    headerArray.append("\n")
    return headerArray

def getContentOfObj(content):
    pass
#splitFunction2()
ParseFuction("0.xml")
#print(root.tag)
#fileName = xmlfile.split('/')[-1]
#get data time
#dateTimeTag = root.find("")
#with open("num.xml", 'w') as f:
#    f.write(header)