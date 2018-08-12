import xml.etree.ElementTree as ET
import os

xmlfile='D:/sdataprj/Full/Full/4G/ERA/4G ERA.xml'
ns = {'es': 'EricssonSpecificAttributes.17.08.xsd',
      'un': 'utranNrm.xsd',
      'xn': 'genericNrm.xsd',
      'gn': 'geranNrm.xsd',
      'nons': 'configData.xsd'}
element_tree = ET.parse(xmlfile)
root = element_tree.getroot()

fileName = xmlfile.split('/')[-1]
#get date time
date = root.find('nons:fileFooter', ns)
dateTime = date.get('dateTime').split(':')[0]
network = '4G'
#take all <vsDataType>
Type = root.findall('.//xn:vsDataType', ns)

typeArray = []
for name in Type:
    typeArray.append(name.text.rstrip())
nameOfObj = list(set(typeArray))


#create parent - child map
parent_map = dict((c, p) for p in root.getiterator() for c in p)

#main function
def WriteToFile():
    
    for dataTypeName in nameOfObj:
        print(dataTypeName)
        arrayOfContent = []
        arrayOfObj = getArray(dataTypeName, Type) #getArray from Type
        for obj in arrayOfObj:
            tempAttrib = parent_map[obj]
            contentOfObj = tempAttrib.find('./es:' + obj.text.rstrip(), ns)
            if contentOfObj == None:
                continue
            arrayOfContent.append(contentOfObj)
       #print(arrayOfContent)
        headerArray = createHeader(arrayOfContent[0]) #array to write as header of file text

        dataArray = []
        for content in arrayOfContent:
            dataArray.append(getContentOfObj(content))

        nameOfOutputFile = "export_" + dataTypeName.split('vsData')[-1].split('\n')[0] + "__" + dateTime + ".txt"
        locationOfOutputFile ="ERA/" + network + "/" + dateTime + "/" + nameOfOutputFile
        if not os.path.exists(os.path.dirname(locationOfOutputFile)):
            try:
                os.makedirs(os.path.dirname(locationOfOutputFile))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
            
        exportFile = open(os.path.abspath(locationOfOutputFile), 'w', encoding='utf-8')
        headerToWrite = "".join(headerArray)
        exportFile.write(headerToWrite)

        contentToWrite = "".join(dataArray)
        #for data in dataArray:
        #    contentToWrite.append(data + "\n")
            #print(data)
        exportFile.write(contentToWrite)
        exportFile.close() 

    subNetworkContentToWrite = findSubNetwork()
    if not subNetworkContentToWrite:
        pass
    else:
        nameOfOutputFile = "export_SubNetwork__" + dateTime + ".txt"
        locationOfOutputFile ="ERA/" + network + "/" + dateTime + "/" + nameOfOutputFile
        exportFile = open(os.path.abspath(locationOfOutputFile), 'w', encoding='utf-8')
        
        exportFile.write(subNetworkContentToWrite)
    print("Parse completed!")

def createHeader(content): #return array of header
    headerArray = []
    headerArray.append("FileName\t")
    headerArray.append("MO\t")
    if not content:
        return "".join(headerArray)
    headerNames = content.findall("./*")

    
    if not headerNames:
        return headerArray
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
def getArray(dataTypeName, Type): #return array of obj from Type
    arrayOfObj = []
    for typeName in Type:
        if typeName.text == dataTypeName:
            arrayOfObj.append(typeName)
    return arrayOfObj

def getContentOfObj(content):
    contentArray = []
    
   # if not content:
    #    return contentArray.append(" ")
    
    contentArray.append(fileName + "\t")
    tempAttrib = parent_map[content]
    vsdt = tempAttrib.find('xn:vsDataType', ns)

    MO = CreateMO(vsdt)
    
    contentArray.append(MO)

    headerNames = content.findall("./*")
    if not headerNames:
        return "".join(contentArray)
    else:
        for headerName in headerNames:    
            elements = headerName.findall("./*")
            if not elements:
                if not headerName.text:
                    contentArray.append("\t")
                else:
                    contentArray.append(headerName.text.rstrip() + "\t")
            else:
                for element in elements:
                    if not element.text:
                        contentArray.append("\t")
                    else:
                        contentArray.append(element.text.rstrip() + "\t")
    contentArray.append("\n")
    
    return "".join(contentArray) 
    #return contentArray



#function to create MO field
def CreateMO(elementObject):
    arrayOfParent = []
    parent = parent_map[parent_map[elementObject]]

    
    while parent.tag != root.find('.//nons:configData', ns).tag:
        
        if parent.tag == root.find('.//xn:VsDataContainer', ns).tag:
            attribOfparent = parent.find('./xn:attributes/xn:vsDataType', ns)
            arrayOfParent.append(attribOfparent.text.rstrip().split('vsData')[-1] + "=" + parent.get('id'))
        else:
            if parent.tag.split('}')[-1] != elementObject.text.rstrip().split('vsData')[-1]:
                arrayOfParent.append(parent.tag.split('}')[-1] + "=" + parent.get('id'))
       
        parent = parent_map[parent]

    arrayOfParent = arrayOfParent[::-1]
    return ",".join(arrayOfParent)

#fucntion to handle SubNetwork
def findSubNetwork():
    headerSubNetwork = ""
    subNetworkContentToWrite = ""
    arrayOfParent = []
    subNetworks = root.findall('.//xn:SubNetwork', ns)
    for subNetwork in subNetworks:
        subNetworkContent = []
        subNetworkContent.append(fileName + "\t")
        attrib = subNetwork.find("./xn:attributes", ns)
        if not attrib:
            subNetworkContentToWrite = subNetworkContentToWrite + subNetworkContent[0] + "\n"
            continue
        else:
            headerSubNetwork = "".join(createHeader(attrib))
            
            parent = subNetwork

            while parent.tag != root.find('.//nons:configData', ns).tag:        
                arrayOfParent.append(parent.tag.split('}')[-1] + "=" + parent.get('id'))
        
                parent = parent_map[parent]

            arrayOfParent = arrayOfParent[::-1]
            subNetworkContent.append(",".join(arrayOfParent) + "\t")
            
            headerNames = attrib.findall("./*")
            if not headerNames:
                pass
            else:
                for headerName in headerNames:    
                    elements = headerName.findall("./*")
                    if not elements:
                        if not headerName.text:
                            subNetworkContent.append("\t")
                        else:
                            subNetworkContent.append(headerName.text.rstrip() + "\t")
                    else:
                        for element in elements:
                            if not element.text:
                                subNetworkContent.append("\t")
                            else:
                                subNetworkContent.append(element.text.rstrip() + "\t")
        
            subNetworkContentToWrite = subNetworkContentToWrite + "".join(subNetworkContent) + "\n"
    return headerSubNetwork + subNetworkContentToWrite    

WriteToFile()
#print(len(getArray("vsDataReportConfigEUtraIntraFreqPm", Type)))
#for i in nameOfObj:
#    print(i)


#a = findSubNetwork()
#print(a)