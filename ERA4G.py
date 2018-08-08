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

#get date time
date = root.find('nons:fileFooter', ns)
dateTime = date.get('dateTime').split(':')[0]
network = '4G'
#take all <vsDataType>
Type = root.findall('.//xn:vsDataType', ns)
typeArray = []
for name in Type:
    typeArray.append(name.text)
nameOfObj = list(set(typeArray))
#print(len(nameOfObj))
#print(Type[100].text)

#create parent - child map
parent_map = dict((c, p) for p in root.getiterator() for c in p)

#main function
def WriteToFile():
    for dataTypeName in nameOfObj:
        #print(dataTypeName)
        arrayOfContent = []
        arrayOfObj = getArray(dataTypeName) #getArray from Type
        for obj in arrayOfObj:
            tempAttrib = parent_map[obj]
            contentOfObj = tempAttrib.find('./es:' + obj.text, ns)
            print(contentOfObj.tag)
            arrayOfContent.append(contentOfObj)
        
        headerArray = createHeader(arrayOfContent[0]) #array to write as header of file text
        dataArray = []
        for content in arrayOfContent:
            dataArray.append(getContentOfObj(content))

        nameOfOutputFile = "export_" + dataTypeName.split('vsData')[-1].split('\n')[0] + "__" + dateTime + ".txt"
        locationOfOutputFile ="ERA/" + network + "/" + dateTime + "/" + nameOfOutputFile
        if not os.path.exists(os.path.dirname(locationOfOutputFile)):
            os.makedirs(os.path.dirname(locationOfOutputFile))
            
        exportFile = open(os.path.abspath(locationOfOutputFile), 'w', encoding='utf-8')
        #exportFile.write("\t".join(headerArray))
        #print(headerArray)
        for data in dataArray:
            #exportFile.write(''.join(data))
            #print(data)
            pass
        exportFile.close() 
        
        

def createHeader(content): #return array of header
    headerArray = []
    if not content:
        return headerArray.append(" ")
    headerNames = content.findall("./*")
    
    headerArray.append("FileName")
    headerArray.append("MO")
    if not headerNames:
        return headerArray.append(" ")
    else:
        for headerName in headerNames:    
            elements = headerName.findall("./*")
            if not elements:
                headerArray.append(headerName.tag.split('}')[-1])
            else:
                currentTagName = headerName.tag.split('}')[-1]
                for element in elements:
                    columnHeader = currentTagName + "_" + element.tag.split('}')[-1]
                    headerArray.append(columnHeader)
    headerArray.append("\n")
    return headerArray
def getArray(dataTypeName): #return array of obj from Type
    arrayOfObj = []
    for typeName in Type:
        if typeName.text == dataTypeName:
            arrayOfObj.append(typeName)
    return arrayOfObj

def getContentOfObj(content):
    contentArray = []
   # if not content:
    #    return contentArray.append(" ")
    fileName = xmlfile.split('/')[-1]
    #print(content.tag)
    tempAttrib = parent_map[content]
    vsdt = tempAttrib.find('xn:vsDataType', ns)
    MO = CreateMO(vsdt)
    contentArray.append(fileName)
    contentArray.append(MO)

    headerNames = content.findall("./*")
    if not headerNames:
        return contentArray.append(" ")
    else:
        for headerName in headerNames:    
            elements = headerName.findall("./*")
            if not elements:
                if not headerName.text:
                    contentArray.append("\t")
                else:
                    contentArray.append(headerName.text + "\t")
            else:
                for element in elements:
                    if not element.text:
                        contentArray.append("\t")
                    else:
                        contentArray.append(element.text + "\t")
    contentArray.append("\n")
    return contentArray








#function to create MO field
def CreateMO(elementObject):

    arrayOfParent = []
    #if not elementObject:
    #   return arrayOfParent.append("invalid element Obj")

    parent = parent_map[parent_map[elementObject]]

    #print(parent.tag)
    while parent.tag != root.find('.//nons:configData', ns).tag:
        #print(parent.attrib)
        if parent.tag == root.find('.//xn:VsDataContainer', ns).tag:
            attribOfparent = parent.find('./xn:attributes/xn:vsDataType', ns)
            arrayOfParent.append(attribOfparent.text.split('vsData')[-1] + "=" + parent.get('id'))
        else:
            if parent.tag.split('}')[-1] != elementObject.text.split('vsData')[-1]:
                arrayOfParent.append(parent.tag.split('}')[-1] + "=" + parent.get('id'))
       
        parent = parent_map[parent]

    arrayOfParent = arrayOfParent[::-1]
    return ",".join(arrayOfParent)

WriteToFile()

